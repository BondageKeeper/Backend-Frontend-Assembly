raw_pipeline_logs = [
    {
        "pipeline_id": "9901",
        "owner": {
            "developer_email": "lead_dev@ai-core.net",
            "tier": "enterprise"
        },
        "agents_chain": [
            {
                "agent_name": "llama-3-planner",
                "role": "planner",
                "execution_metrics": {"duration": "1.52", "tokens_spent": "450"}
            },
            {
                "agent_name": "gpt-4o-coder",
                "role": "coder",
                "execution_metrics": {"duration": "4.15", "tokens_spent": "1200"}
            },
            {
                "agent_name": "gpt-4o-tester",
                "role": "tester",
                "execution_metrics": {"duration": "2.10", "tokens_spent": "800"}
            }
        ]
    },
    {
        "pipeline_id": 9902,
        "owner": {
            "developer_email": "scam_usergmail.com",  #raw gmail
            "tier": "free"
        },
        "agents_chain": [
            {
                "agent_name": "unknown-model",
                "role": "planner",  #forbidden role
                "execution_metrics": {"duration": 0.1, "tokens_spent": 10}
            }
        ]
    }
]
from pydantic import BaseModel , field_validator , computed_field , field_serializer , validate_call , ConfigDict
class ManagerExecutionMetrix(BaseModel):
    duration: float = Field(gt=0)
    tokens_spent: int = Field(ge=0)
    model_config = ConfigDict(extra='forbid')

class ManagerAgentsChain(BaseModel):
    agent_name: str
    role: str
    execution_metrics: ManagerExecutionMetrix
    model_config = ConfigDict(extra='forbid')
    @field_validator('role')
    @classmethod
    def check_role(cls,value:str):
        import re
        if not re.search(r'^(planner|coder|tester)$',value):
            raise ValueError('Warning! Such role is forbidden!')
        return value

class ManagerOwner(BaseModel):
    developer_email: EmailStr
    tier: str
    model_config = ConfigDict(extra='forbid')

class PipelineLogSchema(BaseModel):
    pipeline_id: int = Field(ge=0)
    owner: ManagerOwner
    agents_chain: list[ManagerAgentsChain]
    model_config = ConfigDict(frozen=True)
    @model_validator(mode='after')
    def chain_length(self):
        if self.owner.tier == 'free' and len(self.agents_chain) > 1:
            raise ValueError('You re unable to launch conveyor!')
        return self
    @computed_field(return_type='float')
    @property
    def total_cost(self):
        total_tokens = sum(agent.execution_metrics.tokens_spent * 0.00001 for agent in self.agents_chain)
        return total_tokens * 0.00001
    @field_serializer('total_cost')
    def just_rounding(self,value:float):
        return f'{round(value,3)} USD'

@validate_call
def load_raw_json(log: PipelineLogSchema):
    load = log.model_dump_json(exclude={"owner"})
    print(load)
for raw_dict in raw_pipeline_logs:
    try:
        validated_data = PipelineLogSchema.model_validate(raw_dict)
        load_raw_json(validated_data)
    except Exception as error:
        print(f'*** Error happened: {error} ***')

