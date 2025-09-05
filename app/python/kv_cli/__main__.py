import argparse
import base64
import hashlib
import os
import sys
from datetime import datetime

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient
from azure.keyvault.keys import KeyClient
from azure.keyvault.keys.crypto import CryptographyClient, SignatureAlgorithm
from azure.keyvault.certificates import CertificateClient


def _vault_url_from_name(name: str) -> str:
    if name.startswith("http://") or name.startswith("https://"):
        return name.rstrip('/')
    return f"https://{name}.vault.azure.net"


def _credential(verbose: bool):
    # DefaultAzureCredential works locally with `az login` and in Azure with MI.
    cred = DefaultAzureCredential(exclude_shared_token_cache_credential=True)
    if verbose:
        print("[i] Using DefaultAzureCredential")
    return cred


def cmd_read_secret(args):
    kv_url = _vault_url_from_name(args.vault)
    cred = _credential(args.verbose)
    client = SecretClient(vault_url=kv_url, credential=cred)
    sec = client.get_secret(args.name)
    print("secret.name=", sec.name)
    print("secret.version=", sec.properties.version)
    print("secret.enabled=", sec.properties.enabled)
    print("secret.created_on=", sec.properties.created_on)
    print("secret.updated_on=", sec.properties.updated_on)
    if args.show_value:
        print("secret.value=", sec.value)


def cmd_sign(args):
    kv_url = _vault_url_from_name(args.vault)
    cred = _credential(args.verbose)
    key_client = KeyClient(vault_url=kv_url, credential=cred)
    key = key_client.get_key(args.name)
    kid = key.id
    if args.verbose:
        print("[i] Using key id:", kid)
    crypto = CryptographyClient(key=kid, credential=cred)

    data = args.data.encode("utf-8")
    digest = hashlib.sha256(data).digest()
    result = crypto.sign(SignatureAlgorithm.rs256, digest)
    sig_b64 = base64.b64encode(result.signature).decode("ascii")

    print("kid=", result.key_id)
    print("alg=", result.algorithm)
    print("signature.b64=", sig_b64)


def cmd_show_cert(args):
    kv_url = _vault_url_from_name(args.vault)
    cred = _credential(args.verbose)
    client = CertificateClient(vault_url=kv_url, credential=cred)
    cert = client.get_certificate(args.name)
    props = cert.properties
    thumb = base64.b16encode(props.x509_thumbprint or b"").decode("ascii").lower()
    print("certificate.name=", cert.name)
    print("certificate.version=", props.version)
    print("certificate.enabled=", props.enabled)
    print("certificate.not_before=", props.not_before)
    print("certificate.expires_on=", props.expires_on)
    print("certificate.thumbprint=", thumb)


def build_parser():
    p = argparse.ArgumentParser(
        prog="kv-cli",
        description="Minimal Azure Key Vault CLI for demo (secrets/keys/certs)",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    common = argparse.ArgumentParser(add_help=False)
    common.add_argument(
        "--vault",
        default=os.environ.get("KV_NAME", ""),
        help="Key Vault name or full URL (default from KV_NAME)",
        required=False,
    )
    common.add_argument("--verbose", action="store_true")

    sp = sub.add_parser("read-secret", parents=[common], help="Read a secret by name (no version)")
    sp.add_argument("--name", default=os.environ.get("SECRET_NAME", "demo-secret"))
    sp.add_argument("--show-value", action="store_true", help="Print the secret value (beware in demos)")
    sp.set_defaults(func=cmd_read_secret)

    sp = sub.add_parser("sign", parents=[common], help="Sign payload with a key (RS256)")
    sp.add_argument("--name", default=os.environ.get("KEY_NAME", "demo-key"))
    sp.add_argument("--data", default="hello")
    sp.set_defaults(func=cmd_sign)

    sp = sub.add_parser("show-cert", parents=[common], help="Show certificate metadata")
    sp.add_argument("--name", default=os.environ.get("CERT_NAME", "demo-cert"))
    sp.set_defaults(func=cmd_show_cert)

    return p


def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)
    if not args.vault:
        print("[!] --vault is required (or set KV_NAME)")
        return 2
    try:
        return args.func(args) or 0
    except Exception as ex:
        print(f"[!] Error: {ex}")
        if getattr(args, 'verbose', False):
            raise
        return 1


if __name__ == "__main__":
    sys.exit(main())

