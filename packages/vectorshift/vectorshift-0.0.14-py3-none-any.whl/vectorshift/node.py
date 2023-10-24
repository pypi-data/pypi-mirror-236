# functionality defining the shape and properties of computation nodes, and how
# they connect to each other in pipelines
from abc import ABC, abstractclassmethod
import json
import re
import requests

import vectorshift
from vectorshift.consts import *

# A parent class for all nodes. Shouldn't be initialized by the user directly.
class NodeTemplate(ABC):
    # TODO: think about where we might want to use @property.
    # TODO: right now some subclasses support an optional typechecking flag in
    # case we want to do future typchecking. See the pattern below of checking
    # if _typecheck is in kwargs. If we stick with this pattern, SDK users
    # shouldn't know that the _typecheck arg exists.
    def __init__(self):
        # Each node has a certain type, also called an "ID" in Mongo. The _id
        # of the node is formed by appending a counter to the node type.
        self.node_type:str = None
        self._id:str = None
        # Every node has zero or more inputs or outputs. Each output itself 
        # is a list (in case one input takes in/aggregates multiple outputs)
        self._inputs:dict[str, list[NodeOutput]] = {}
        
    # Inputs are a dictionary of NodeOutputs keyed by input fields (the in-edge 
    # labels in the no-code graph/the target handle for the node's in-edge).
    def inputs(self): return self._inputs
    
    # Outputs should be a dictionary of NodeOutputs keyed by output fields (the
    # out-edge labels/the source handle for the node's out-edge). Invariant: 
    # a key should equal the corresponding value's output_field.
    # For syntactic sugar, class-specific methods can also return specific 
    # outputs rather than the entire dict, e.g. the method "output()" that 
    # directly gives the NodeOutput object for nodes that only have one output.
    def outputs(self): raise NotImplementedError("Subclasses should implement this!")

    # The dictionary that corresponds with the JSON serialization of the node. 
    # This should return a subset of how a node object is stored as part of a
    # pipeline in Mongo, specifically, the following attributes: type, id, and
    # data (and all subfields therein). This should only be called after an id
    # has been assigned to the node.
    # NB: the JSON fields id/data.id and type/data.nodeType are the same.
    @abstractclassmethod
    def to_json_rep(self):
        # If the node references a user-defined object that lives on the VS
        # platform (other pipelines, integrations, files, vectorstores,
        # transformations), calling this function will involve an API call
        # to get the details of that user-defined object.
        raise NotImplementedError("Subclasses should implement this!")
    
    # From a Python dict representing how a node is stored in JSON, create a
    # node object. IMPORTANTLY, this does NOT initialize the _inputs param 
    # with NodeOutput values (and thus doesn't perform typechecks); we expect 
    # NodeOutputs to be inserted post_hoc, and assume they're valid.
    @staticmethod
    @abstractclassmethod
    def _from_json_rep(json_data:dict):
        _ = json_data # if linter complains
        raise NotImplementedError("Subclasses should implement this!")
    
    @classmethod 
    def from_json_rep(cls, json_data: dict):
        n : NodeTemplate = cls._from_json_rep(json_data)
        n._id = json_data["id"]
        n._inputs = {k: [] for k in n._inputs.keys()}
        return n
    
    def __str__(self): return json.dumps(self.to_json_rep())

# A wrapper class for outputs from nodes, for basic "type"-checks and to figure
# out how nodes connect to each other. NOT the same as OutputNode, which is 
# a node that represents the final result of a pipeline.
class NodeOutput:
    def __init__(self, source:NodeTemplate, output_field:str, output_type:str):
        # The Node object producing this output.
        self.source = source
        # The specific output field from the source node (the node handle).
        self.output_field = output_field
        # A string roughly corresponding to the output type. (Strings are 
        # flimsy, but they will do the job.) TODO: This isn't really used now, 
        # but in the future this field could be used to ascribe general data 
        # types to outputs for better "type"-checking if needed.
        self.output_type = output_type
    def __str__(self):
        return f"Node output of type {self.output_type}"

# Each node subclasses NodeTemplate and takes in class-specific parameters 
# depending on what the node does. Node classes below are organized by their
# order and structure of appearance in the no-code editor.

# Let's try to avoid more than one level of subclassing.

###############################################################################
# HOME                                                                        #
###############################################################################

# Input nodes themselves don't have inputs; they define the start of a pipeline.
class InputNode(NodeTemplate):
    def __init__(self, name:str, input_type:str):
        super().__init__()
        self.node_type = "customInput"
        self.name = name
        # Text or File
        if input_type not in INPUT_NODE_TYPES:
            raise ValueError(f"Input node type {input_type} not supported.")
        self.input_type = input_type
        
    def output(self): 
        # Input nodes can produce anything in INPUT_NODE_TYPES, so we mark
        # the specific type here.
        return NodeOutput(
            source=self, 
            output_field="value", 
            output_type=self.input_type
        )
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def to_json_rep(self):
        # TODO: category and task_name can probably be made into class variables too.
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "inputName": self.name,
                "inputType": self.input_type.capitalize(),
                "category": "input",
                "task_name": "input"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return InputNode(
            name=json_data["data"]["inputName"], 
            input_type=json_data["data"]["inputType"].lower()
        )

# Outputs are the end of the pipeline and so only take inputs.
class OutputNode(NodeTemplate):
    def __init__(self, name:str, output_type:str, input:NodeOutput):
        super().__init__()
        self.node_type = "customOutput"
        self.name = name
        # Text or File
        if output_type not in OUTPUT_NODE_TYPES:
            raise ValueError(f"Output node type {output_type} not supported.")
        self.output_type = output_type
        self._inputs = {"value": [input]}

    def outputs(self): return None
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "outputName": self.name,
                "outputType": self.output_type.capitalize(),
                "category": "output",
                "task_name": "output"
            }
        }
        
    @staticmethod 
    def _from_json_rep(json_data:dict):
        return OutputNode(
            name=json_data["data"]["outputName"], 
            output_type=json_data["data"]["outputType"].lower(),
            input=None
        )

# Text data. This is possibly even a little redundant because we can pass in
# plaintext inputs as additional params to nodes (without instantiating them
# as separate nodes) through code. Right now though I'm trying to get a 1:1 
# correspondance between no-code and code construction; we can discuss this.
class TextNode(NodeTemplate):
    # Text nodes can either just be blocks of text in themselves, or also take
    # other text nodes as inputs (e.g. with text variables like {{Context}}, 
    # {{Task}}). In the latter case, an additional argument text_inputs should
    # be passed in as a dict of input variables to Outputs.
    def __init__(self, text:str, text_inputs:dict[str, NodeOutput] = None, **kwargs):
        super().__init__()
        self.node_type = "text"
        self.text = text
        # if there are required inputs, they should be of the form {{}} - each
        # of them is a text variable
        text_vars = re.findall(r'\{\{([^{}]+)\}\}', self.text)
        text_vars = [v.strip() for v in text_vars]
        self.text_vars = []
        # remove duplicates while preserving order
        [self.text_vars.append(v) for v in text_vars if v not in self.text_vars]
        
        # if there are variables, we expect them to be matched with inputs
        # they should be passed in a dictionary with the
        # arg name text_inputs. E.g. {"Context": ..., "Task": ...}
        if text_inputs:
            if type(text_inputs) != dict:
                raise TypeError("text_inputs must be a dictionary of text variables to node outputs.")
            # TODO: if we want typechecking, we pass in a special arg (never 
            # used right now as we haven't fully spec'd how type checks work).
            if "_typecheck" in kwargs and kwargs["_typecheck"]:
            # example type check: input variables should correspond to text
                for output in text_inputs.values():
                    if output.output_type != "text":
                        raise ValueError("Values in text_inputs must have type 'text'.")
            num_inputs = len(text_inputs.keys())
            num_vars = len(self.text_vars)
            if num_inputs != num_vars:
                raise ValueError(f"Number of text inputs ({num_inputs}) does not match number of text variables ({num_vars}).")
            if sorted(list(set(text_inputs.keys()))) != sorted(self.text_vars):
                raise ValueError("Names of text inputs and text variables do not match.")
            # wrap each NodeOutput into a singleton list to fit the type
            self._inputs = {k: [v] for k, v in text_inputs.items()}
        else:
            if len(self.text_vars) > 0:
                raise ValueError("text_inputs must be passed in if there are text variables.")
            
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
        
    def to_json_rep(self):
        input_names = self.text_vars if len(self.text_vars) > 0 else None
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "text": self.text,
                "inputNames": input_names,
                "formatText": True,
                "category": "task",
                "task_name": "text",
            } 
        }
        
    def _from_json_rep(json_data:dict):
        text_inputs = None
        if json_data["data"]["inputNames"]:
            text_inputs = {}
            for name in json_data["data"]["inputNames"]:
                text_inputs[name] = None
        return TextNode(
            text=json_data["data"]["text"],
            text_inputs=text_inputs
        )

# Nodes representing file data, taking no inputs.
### USES USER-CREATED OBJECT
class FileNode(NodeTemplate):
    def __init__(self):
        super().__init__()
        self.node_type = "todo"
        raise NotImplementedError
    
    def outputs(self):
        raise NotImplementedError
    
    def to_json_rep(self):
        raise NotImplementedError

# Nodes representing entire other pipelines, a powerful tool for abstraction.
# When the node is executed, the pipeline it represents is executed with the
# supplied inputs, and the overall pipeline's output becomes the node's output.
### USES USER-CREATED OBJECT
class PipelineNode(NodeTemplate):
    def __init__(self):
        super().__init__()
        self.node_type = "todo"
        raise NotImplementedError
    
    def outputs(self):
        raise NotImplementedError
    
    def to_json_rep(self):
        raise NotImplementedError
    
# Integrations with third parties.
### USES USER-CREATED OBJECT
class IntegrationNode(NodeTemplate):
    def __init__(self):
        super().__init__()
        self.node_type = "todo"
        raise NotImplementedError
    
    def outputs(self):
        raise NotImplementedError
    
    def to_json_rep(self):
        raise NotImplementedError

### USES USER-CREATED OBJECT    
class TransformationNode(NodeTemplate):
    def __init__(self):
        super().__init__()
        self.node_type = "todo"
        raise NotImplementedError
    
    def outputs(self):
        raise NotImplementedError
    
    def to_json_rep(self):
        raise NotImplementedError

# File save nodes have no outputs.
class FileSaveNode(NodeTemplate):
    def __init__(self, name_input:NodeOutput, files_input:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = "fileSave"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if name_input.output_type != "text":
                raise ValueError("Name must be of type text.")
        self._inputs = {
            "name": [name_input],
            # files aggregates one or more node outputs
            "files": files_input
        }
    
    def outputs(self): return None
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "category": "task",
                "task_name": "save_file"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        _ = json_data 
        return FileSaveNode(
            name_input=None,
            files_input=[]
        )

###############################################################################
# LLMS                                                                        #
###############################################################################

class OpenAILLMNode(NodeTemplate):
    def __init__(self, model:str, system_input:NodeOutput, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "llmOpenAI"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            # example simple type-check: inputs should be text
            if system_input.output_type != "text" or prompt_input.output_type != "text":
                raise ValueError("LLM inputs must be text.")
        if model not in SUPPORTED_OPENAI_LLMS.keys():
            raise ValueError(f"Invalid model {model}.")
        self.model = model 
        # the user might have passed in more model params through kwargs
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ["max_tokens", "temperature", "top_p"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        if self.max_tokens > SUPPORTED_OPENAI_LLMS[self.model]:
            raise ValueError(f"max_tokens {self.max_tokens} is too large for model {self.model}.")
        self._inputs = {"system": [system_input], "prompt": [prompt_input]}
    
    def output(self): 
        return NodeOutput(source=self, output_field="response", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "maxTokens": self.max_tokens,
                "temperature": str(round(self.temp, 2)),
                "topP": str(round(self.top_p, 2)),
                "category": "task",
                "task_name": "llm_openai"
            }
        }
       
    @staticmethod 
    def _from_json_rep(json_data:dict):
        return OpenAILLMNode(
            model=json_data["data"]["model"],
            system_input=None,
            prompt_input=None,
            max_tokens=json_data["data"]["maxTokens"],
            temperature=float(json_data["data"]["temperature"]),
            top_p=float(json_data["data"]["topP"])
        )
        
class AnthropicLLMNode(NodeTemplate):
    def __init__(self, model:str, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "llmAnthropic"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if prompt_input.output_type != "text":
                raise ValueError("LLM inputs must be text.")
        if model not in SUPPORTED_ANTHROPIC_LLMS.keys():
            raise ValueError(f"Invalid model {model}.")
        self.model = model 
        self.max_tokens, self.temp, self.top_p = 1024, 1., 1.
        for optional_param_arg in ["max_tokens", "temperature", "top_p"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        if self.max_tokens > SUPPORTED_OPENAI_LLMS[self.model]:
            raise ValueError(f"max_tokens {self.max_tokens} is too large for model {self.model}.")
        self._inputs = {"prompt": [prompt_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="response", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "maxTokens": self.max_tokens,
                "temperature": str(round(self.temp, 2)),
                "topP": str(round(self.top_p, 2)),
                "category": "task",
                "task_name": "llm_anthropic"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return AnthropicLLMNode(
            model=json_data["data"]["model"],
            prompt_input=None,
            max_tokens=json_data["data"]["maxTokens"],
            temperature=float(json_data["data"]["temperature"]),
            top_p=float(json_data["data"]["topP"])
        )

###############################################################################
# MULTIMODAL                                                                  #
###############################################################################

class ImageGenNode(NodeTemplate):
    def __init__(self, model:str, image_size:int, num_images:int, prompt_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "imageGen"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if prompt_input.output_type != "text":
                raise ValueError("Image generation inputs must be text.")
        if model not in SUPPORTED_IMAGE_GEN_MODELS.keys():
            raise ValueError(f"Invalid model {model}.")
        self.model = model
        if image_size not in SUPPORTED_IMAGE_GEN_MODELS[self.model][0]:
            raise ValueError(f"Invalid image size {image_size}.")
        if num_images not in SUPPORTED_IMAGE_GEN_MODELS[self.model][1]:
            raise ValueError(f"Invalid number of images {num_images}.")
        self.image_size = image_size 
        self.num_images = num_images 
        self._inputs = {"prompt": [prompt_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="images", output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "size": f"{self.image_size}x{self.image_size}",
                "imageCount": self.num_images,
                "category": "task",
                "task_name": "generate_image"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        image_size_str = json_data["data"]["size"]
        image_size = int(image_size_str[:image_size_str.index('x')])
        return ImageGenNode(
            model=json_data["data"]["model"],
            image_size=image_size,
            num_images=int(json_data["data"]["imageCount"]),
            prompt_input=None,
        )
    
class SpeechToTextNode(NodeTemplate):
    def __init__(self, model:str, audio_input:NodeOutput):
        super().__init__()
        self.node_type = "speechToText"
        if model not in SUPPORTED_SPEECH_TO_TEXT_MODELS:
            raise ValueError(f"Invalid model {model}.")
        self.model = model
        self._inputs = {"audio": [audio_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="text", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "model": self.model,
                "category": "task",
                "task_name": "speech_to_text"
            }
        }
        
    @staticmethod 
    def _from_json_rep(json_data:dict):
        return SpeechToTextNode(
            model=json_data["data"]["model"],
            audio_input=None
        )

###############################################################################
# DATA LOADERS                                                                #
###############################################################################

# The specific data loaded by the nodes is given by the class name.
# TODO: Right now we have a different class to represent each type of data 
# loader available in the no-code platform. I think this could be significantly
# abstracted since most of the internal logic is the same.

class FileLoaderNode(NodeTemplate):
    def __init__(self, file_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if file_input.output_type != "InputNode.file":
                raise ValueError("Must take a file from an input node.")
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"file": [file_input]}
                
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "File",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_file"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return FileLoaderNode(
            file_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class CSVQueryNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, csv_input:NodeOutput, **kwargs):
        super().__init__()
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if query_input.output_type != "text":
                raise ValueError("CSV query input must have type 'text'.")
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input], "csv": [csv_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output() 
        return {o.output_field: o}

    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "CSV Query",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "query_csv"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return CSVQueryNode(
            query_input=None,
            csv_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class URLLoaderNode(NodeTemplate):
    # TODO: does this node need chunk params?
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"url": [url_input]}
    
    def output(self): 
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "URL",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_url"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return URLLoaderNode(
            url_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
        
class WikipediaLoaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Wikipedia",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_wikipedia"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return WikipediaLoaderNode(
            query_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
    
class YouTubeLoaderNode(NodeTemplate):
    def __init__(self, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"url": [url_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "YouTube",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_youtube"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return YouTubeLoaderNode(
            url_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
    
class ArXivLoaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Arxiv",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_arxiv"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return ArXivLoaderNode(
            query_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class SerpAPILoaderNode(NodeTemplate):
    def __init__(self, api_key_input:NodeOutput, query_input:NodeOutput, **kwargs):
        super().__init__()
        if "_typecheck" in kwargs and kwargs["_typecheck"]:
            if api_key_input.output_type != "text":
                raise ValueError("API key input must have type text.")
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"apiKey": [api_key_input], "query": [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "SerpAPI",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_serpapi"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        return SerpAPILoaderNode(
            api_key_input=None,
            query_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class GitLoaderNode(NodeTemplate):
    def __init__(self, repo_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"repo": [repo_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Git",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_git"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return GitLoaderNode(
            repo_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class NotionLoaderNode(NodeTemplate):
    def __init__(self, token_input:NodeOutput, database_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"token": [token_input], "database": [database_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Notion",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_notion"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return NotionLoaderNode(
            token_input=None,
            database_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )
    
class ConfluenceLoaderNode(NodeTemplate):
    def __init__(self, username_input:NodeOutput, api_key_input:NodeOutput, url_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "dataLoader"
        self.chunk_size, self.chunk_overlap, self.func = 400, 0, "default"
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {
            "username": [username_input],
            "apiKey": [api_key_input],
            "url": [url_input]
        }
    
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "loaderType": "Confluence",
                "function": self.func,
                "chunkSize": self.chunk_size,
                "chunkOverlap": self.chunk_overlap,
                "category": "task",
                "task_name": "load_confluence"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return ConfluenceLoaderNode(
            username_input=None,
            api_key_input=None,
            url_input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

###############################################################################
# VECTORDB                                                                    #
###############################################################################

class VectorDBLoaderNode(NodeTemplate):
    def __init__(self, documents_input:list[NodeOutput], **kwargs):
        super().__init__()
        self.node_type = "vectorDBLoader"
        self.func, self.chunk_size, self.chunk_overlap = "default", 400, 0
        for optional_param_arg in ["chunk_size", "chunk_overlap", "func"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"documents": documents_input}
    
    def output(self):
        return NodeOutput(source=self, output_field="database", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": self.func,
                "category": "task",
                "task_name": "load_vector_db"
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return VectorDBLoaderNode(
            input=None,
            chunk_size=json_data["data"]["chunkSize"],
            chunk_overlap=json_data["data"]["chunkOverlap"],
            func=json_data["data"]["function"]
        )

class VectorDBReaderNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, database_input:NodeOutput, **kwargs):
        super().__init__()
        self.node_type = "vectorDBReader"
        self.func, self.max_docs_per_query = "default", 2
        for optional_param_arg in ["func", "max_docs_per_query"]:
            if optional_param_arg in kwargs:
                setattr(self, optional_param_arg, kwargs[optional_param_arg])
        self._inputs = {"query": [query_input], "database": [database_input]}
    
    def output(self):
        # assume the reader returns the query result post-processed back into text
        return NodeOutput(source=self, output_field="results", output_type="text")
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": self.func,
                "category": "task",
                "task_name": "query_vector_db",
                "maxDocsPerQuery": self.max_docs_per_query
            }
        }
        
    @staticmethod
    def _from_json_rep(json_data:dict):
        return VectorDBReaderNode(
            query_input=None,
            database_input=None,
            func=json_data["data"]["function"],
            max_docs_per_query=json_data["data"]["maxDocsPerQuery"]
        )
        
class VectorStoreNode(NodeTemplate):
    def __init__(self, query_input:NodeOutput, public_key:str, private_key:str,
                 vectorstore_id=None, vectorstore_name=None, 
                 username=None, org_name=None, max_docs_per_query=1):
        super().__init__()
        self.node_type = 'vectorStore'
        if vectorstore_id is None and vectorstore_name is None:
            raise ValueError('Either the vectorstore ID or name should be specified.')
        self.vectorstore_id = vectorstore_id
        self.vectorstore_name = vectorstore_name
        self.username = username 
        self.org_name = org_name
        self.max_docs_per_query = max_docs_per_query
        # we'll need to use the API key when fetching the user-defined 
        # vectorstore
        self._public_key = public_key or vectorshift.public_key
        self._private_key = private_key or vectorshift.private_key
        # we don't store vectorstore-specific params like chunk params, since 
        # that is a property of the vectorstore and not the node
        self._inputs = {'query': [query_input]}
    
    def output(self):
        return NodeOutput(source=self, output_field='results', output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    # If this node was loaded from JSON and changed to reference another
    # vectorstore object, we need to use the API key to query the new object.
    # This setter provides an explicit way to make sure the API key is in the 
    # node (if the key weren't initialized globally).
    def set_api_key(self, public_key:str, private_key:str):
        self._public_key = public_key
        self._private_key = private_key
    
    def to_json_rep(self):
        if self._public_key is None or self._private_key is None:
            raise ValueError('API key required to fetch vectorstore.')
        # There's currently no notion of "sharing" vectorstores (so username
        # and org_name aren't required right now), but there probably will be 
        # one in the future.
        response = requests.get(
            API_VECTORSTORE_FETCH_ENDPOINT,
            data={
                'vectorstore_id': self.vectorstore_id,
                'vectorstore_name': self.vectorstore_name,
                'username': self.username,
                'org_name': self.org_name
            },
            headers={
                'Public-Key': self._public_key,
                'Private-Key': self._private_key
            }
        )
        if response.status_code != 200:
            raise Exception(f"Error fetching vectorstore: {response.text}")
        vectorstore_json = response.json()
        return {
            'id': self._id,
            'type': self.node_type,
            'data': {
                'id': self._id, 
                'nodeType': self.node_type,
                'maxDocsPerQuery': self.max_docs_per_query,
                # we just copy everything over, including the vectors (if any)
                'vectorStore': vectorstore_json,
                'category': 'task',
                'task_name': 'query_vectorstore'
            }
        }

    @staticmethod 
    def _from_json_rep(json_data:dict):
        # there isn't a way to recover the API key from the JSON rep; it can
        # be set with set_api_key; also as mentioned above, (author) username
        # and org name data isn't currently saved in Mongo
        return VectorStoreNode(
            query_input=None,
            vectorstore_id=json_data['data']['vectorStore']['id'],
            vectorstore_name=json_data['data']['vectorStore']['name'], 
            max_docs_per_query=json_data['data']['maxDocsPerQuery']
        )

###############################################################################
# LOGIC                                                                       #
###############################################################################

# NB: To establish that these nodes specifically represent logic/control flow,
# these class names are prefixed with "Logic".
class LogicConditionNode(NodeTemplate):
    # inputs should comprise all in-edges, which are the names of all conditions 
    # and values along with the NodeOutputs they correspond to.
    # conditions is a list of (cond, val), where if cond is True the node 
    # returns val (where val is an input name).
    # default is what the node returns in the (final) else case.
    def __init__(self, inputs:list[tuple[str, NodeOutput]], 
                 conditions:list[tuple[str, str]], else_value:str):
        super().__init__()
        self.node_type = "condition"
        input_names = [i[0] for i in inputs]
        if len(set(input_names)) != len(input_names):
            raise ValueError("Duplicate input names.")
        for cond in conditions:
            if cond[1] not in input_names:
                raise ValueError(f"Returned value {cond[1]} of condition {cond[0]} was not specified in inputs.")
        if else_value not in input_names:
            raise ValueError(f"Returned value {else_value} of else condition was not specified in inputs.")
        self.input_names = input_names
        self.conditions = conditions
        # NB: self.predicates maps to the JSON "conditions" field. The result
        # of the corresponding predicate in the input argument conditions is
        # the same-indexed element in self.output_names.
        self.predicates = [cond[0] for cond in conditions]
        self.output_names = [cond[1] for cond in conditions] + [else_value]
        # each separate input is an in-edge to the node, with the input name
        # being the user-provided name
        self._inputs = {i[0]: [i[1]] for i in inputs}
    
    # Unlike most other nodes, this node has several outputs, corresponding to
    # each of the specified conditions (and the else case).
    def outputs(self):
        # the outputs are labelled "output-0", "output-1", etc. followed by
        # "output-else"
        os = {}
        for ind in range(len(self.predicates)):
            o = NodeOutput(
                source=self, 
                output_field=f"output-{ind}", 
                # TODO: we can get the output type by indexing into 
                # self.conditions[ind][1] to get the variable name,
                # indexing into self._inputs with that name, and accessing
                # the corresponding NodeOutput's output_type
                output_type=None)
            os[o.output_field] = o
        else_o = NodeOutput(source=self, output_field="output-else", output_type=None)
        os[else_o.output_field] = else_o
        return os
    
    # If a user currently wants to index into a specific output, they need to 
    # call the outputs() method and then index into it by name (e.g. 
    # "output-2", "output-else"), or use the helper functions below.
    # TODO: is there a better way to do this?
    def output_index(self, i:int) -> NodeOutput:
        if i < 0 or i >= len(self.predicates):
            raise ValueError("Index out of range.")
        os = self.outputs()
        return os[f"output-{i}"]
    
    def output_else(self) -> NodeOutput: 
        os = self.outputs()
        return os["output-else"]
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "conditions": self.predicates,
                "inputNames": self.input_names,
                "outputs": self.output_names,
                "category": "condition"
            }
        }

    @staticmethod
    def _from_json_rep(json_data:dict):
        predicates = json_data["data"]["conditions"]
        output_names = json_data["data"]["outputs"]
        return LogicConditionNode(
            inputs=[(name, None) for name in json_data["data"]["inputNames"]],
            conditions=[(predicates[i], output_names[i]) for i in range(len(predicates))],
            else_value=output_names[-1]
        )
    
class LogicMergeNode(NodeTemplate):
    def __init__(self, inputs:list[NodeOutput]):
        super().__init__()
        self.node_type = "merge"
        self._inputs = {
            # The JSON name for the in-edge is "input", although the displayed
            # name is "inputs".
            "input": inputs
        }
        
    def output(self):
        return NodeOutput(source=self, output_field="output", output_type=None)
    
    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "function": "default",
                "category": "merge"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        _ = json_data
        return LogicMergeNode(
            inputs=[]
        )

###############################################################################
# CHAT                                                                        #
###############################################################################

class ChatMemoryNode(NodeTemplate):
    # Chat memory nodes don't take input
    def __init__(self, memory_type:str, **kwargs):
        super().__init__()
        if memory_type not in CHAT_MEMORY_TYPES:
            raise ValueError(f"Invalid chat memory type {memory_type}.")
        self.node_type = "chatMemory"
        self.memory_type = memory_type
        self.memory_window_values = {
            # for full text, memory_window isn't used (just take the full text)
            # TODO: confirm this is the right behavior with Alex
            CHAT_MEMORY_TYPES[0]: 0,
            CHAT_MEMORY_TYPES[1]: 0,
            CHAT_MEMORY_TYPES[2]: 10,
            CHAT_MEMORY_TYPES[3]: 2048
        }
        # self.memory_window is set to the value corresponding to 
        # self.memory_type's entry in memory_window_values, which may be 
        # overridden by the constructor arg memory_window
        if "memory_window" in kwargs:
            if self.memory_type in CHAT_MEMORY_TYPES[:2]:
                raise ValueError("Memory window shouldn't be specified if the chat memory is the full text.")
            self.memory_window_values[self.memory_type] = kwargs["memory_window"]
        self.memory_window = self.memory_window_values[self.memory_type]
    
    def output(self):
        return NodeOutput(source=self, output_field="value", output_type=None)

    def outputs(self):
        o = self.output()
        return {o.output_field: o}
    
    def to_json_rep(self):
        return {
            "id": self._id,
            "type": self.node_type,
            "data": {
                "id": self._id,
                "nodeType": self.node_type,
                "memoryType": self.memory_type,
                "memoryWindow": self.memory_window,
                "memoryWindowValues": self.memory_window_values,
                "category": "memory",
                "task_name": "load_memory"
            }
        }
    
    @staticmethod
    def _from_json_rep(json_data:dict):
        n = ChatMemoryNode(
            memory_type=json_data["data"]["memoryType"]
        )
        # overwrite with JSON values
        n.memory_window = json_data["data"]["memoryWindow"]
        n.memory_window_values = json_data["data"]["memoryWindowValues"]
        return n