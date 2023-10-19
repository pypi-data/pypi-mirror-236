import hashlib
from dataclasses import dataclass, field, InitVar
from typing import Union, Any, Optional
from verifyaname.helpers import encode_length_prefixed, Base64UrlSafe


TXT_VERIFICATION_KEY = "fetch-aname-token"
CHAIN_ID = "verification"


@dataclass(frozen=True)
class VerificationTokenData:
    domain: str
    owner_address: Union[str, Any]

    # *AUTO-initialised* data members = they can *NOT* be initialised from init(...) by design.
    # The `hash` & `compare` are set to `True` for both fields, however, strictly speaking, it is not necessary.
    # They are set to `True` only in order to make absolutely sure, that if the values of these fields are manipulated
    # via the `object.__setattr__(...)`, it will affect hash of the object & comparison operator (both used in
    # dictionaries and sets).
    token_raw: bytes = field(default=None, init=False, repr=True, hash=True, compare=True, metadata=None, kw_only=False)
    token: str = field(default=None, init=False, repr=True, hash=True, compare=True, metadata=None, kw_only=False)

    def __post_init__(self):
        if not isinstance(self.owner_address, str):
            object.__setattr__(self, 'owner_address', str(self.owner_address))

        token_raw = self.generate_token(domain=self.domain, owner_address=self.owner_address)
        token = Base64UrlSafe.encode(token_raw)

        object.__setattr__(self, 'token_raw', token_raw)
        object.__setattr__(self, 'token', token)

    def verify(self, token: Union[bytes, str]) -> bool:
        if isinstance(token, str):
            return self.token == token

        if isinstance(token, bytes):
            return self.token_raw == token

        return False

    def verify_dns_txt_record(self, dns_txt: str) -> bool:
        token_b64 = self.extract_token_from_dns_txt_record(dns_txt)
        return self.verify(token_b64)

    def create_dns_txt_record(self) -> str:
        return f'{TXT_VERIFICATION_KEY}={self.token}'

    @staticmethod
    def generate_token(domain: str, owner_address: str) -> bytes:
        hasher = hashlib.sha256()
        hasher.update(encode_length_prefixed(domain))
        hasher.update(encode_length_prefixed(owner_address))
        return hasher.digest()

    @staticmethod
    def extract_token_from_dns_txt_record(dns_txt: str) -> Optional[str]:
        start_idx = dns_txt.find("=")
        if start_idx == -1:
            return None

        key = dns_txt[:start_idx]

        if key == TXT_VERIFICATION_KEY:
            return dns_txt[start_idx+1:]

        return None
