



from enum import Enum
from pydantic import BaseModel


class GatheringSkill(Enum):
    mining = 'mining'
    woodcutting = 'woodcutting'
    fishing = 'fishing'
    alchemy = 'alchemy'


class ResourceSchema(BaseModel):
    name: str = Field(..., description='The name of the resource', title='Name')
    code: str = Field(
        ...,
        description="The code of the resource. This is the resource's unique identifier (ID).",
        title='Code',
    )
    skill: GatheringSkill = Field(
        ...,
        description='The skill required to gather this resource.',
        title='Skill code',
    )
    level: int = Field(
        ...,
        description='The skill level required to gather this resource.',
        title='Level',
    )
    drops: List[DropRateSchema] = Field(
        ..., description='The drops of this resource.', title='Drops'
    )

