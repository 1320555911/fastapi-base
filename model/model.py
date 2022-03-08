"""
    Common model
"""

from pydantic import Field, BaseModel

from utils.ret_code import C_SUCCESS


class MID(BaseModel):
    id: str = Field('', title='ID')


class MTimeC(BaseModel):
    t_created: str = Field('', title='创建时间')


class MTimeU(BaseModel):
    t_updated: str = Field('', title='更新时间')


class MTimeD(BaseModel):
    t_deleted: str = Field('', title='删除时间')


class MTime(MTimeC, MTimeU, MTimeD):
    ...


class MRsp(BaseModel):
    code: int = Field(C_SUCCESS, title='返回码', description=str(CODE_DESC))
    msg: str = Field('', title='返回信息')


class MPagination(BaseModel):
    index: int = Field(..., ge=1, title='当前页码')
    num: int = Field(..., ge=1, title='每页数量')


class MPage(BaseModel):
    index: int = Field(..., title='当前页码')
    total: int = Field(..., title='总数量')
    data: list = Field([], title='本页数据')
