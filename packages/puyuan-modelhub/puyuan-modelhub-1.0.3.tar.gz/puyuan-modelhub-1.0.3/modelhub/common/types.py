from pydantic import BaseModel
from typing import Dict, Optional, Any, List


class GenerationParams(BaseModel):
    """
    GenerationParams: Parameters for text generation
    """

    inputs: str
    """inputs: the input text"""
    parameters: Dict[str, Any] = {}
    """parameters: the parameters for the model"""


class TextGenerationStreamToken(BaseModel):
    """TextGenerationStreamToken: A token in the text generation stream"""

    id: int
    """id: the token id"""
    text: str
    """text: the token text"""
    logprob: float
    """logprob: the log probability of the token"""
    special: bool
    """special: whether the token is a special token"""


class TextGenerationStreamDetails(BaseModel):
    """TextGenerationStreamDetails: Details of the text generation stream"""

    finish_reason: Optional[str] = None
    """finish_reason: the reason for finishing the generation"""
    prompt_tokens: Optional[int] = None
    """prompt_tokens: the number of tokens in the prompt"""
    generated_tokens: Optional[int] = None
    """generated_tokens: the number of tokens generated"""
    seed: Optional[int] = None
    """seed: the seed for the generation"""
    tokens: Optional[List[TextGenerationStreamToken]] = None
    """tokens: the tokens in the generation stream"""


class TextGenerationStreamOutput(BaseModel):
    """TextGenerationStreamOutput: Output of the text generation stream"""

    token: TextGenerationStreamToken
    """token: the token generated"""
    generated_text: Optional[str] = None
    """generated_text: the generated text"""
    details: Optional[TextGenerationStreamDetails] = None
    """details: the details of the generation stream"""


class TextGenerationOutput(BaseModel):
    """TextGenerationOutput: Output of text generation"""

    generated_text: str
    """generated_text: the generated text"""
    details: Optional[TextGenerationStreamDetails] = None
    """details: the details of the generation stream"""


class EmbeddingOutput(BaseModel):
    """EmbeddingOutput: Output of text embedding"""

    embeddings: List[List[float]] | List[float]
    """embeddings: the embeddings of the text"""
