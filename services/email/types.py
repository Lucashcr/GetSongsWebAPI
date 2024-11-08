from typing import Optional, TypedDict, Union


class EmailServiceInitOptions(TypedDict):
    from_email: Optional[str]
    to_emails: Union[list[str], str]
    subject: str
    body: str
