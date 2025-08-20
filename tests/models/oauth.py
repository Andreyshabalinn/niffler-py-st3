from pydantic import BaseModel


class OAuthRequest(BaseModel):
    response_type: str = "code"
    client_id: str = "client"
    scope: str = "openid"
    redirect_uri: str
    code_challenge: str
    code_challenge_method: str = "S256"