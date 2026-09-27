#!/usr/bin/env python3
"""Sync Chinese OpenAPI specs from the AuthMS monorepo into this portal.

Source: D:\\go\\auth_ms_new\\docker\\specs\\<service>\\swagger.json (Chinese, native)
Target: public/specs/<service>.json

The generator's own English exports live next to the Chinese ones as
`*-en.json`; this portal serves the Chinese originals instead.

Usage:
    python scripts/sync-specs-zh.py
"""

import json
import os
import sys

sys.stdout.reconfigure(encoding="utf-8")

SPECS_SRC = r"D:\go\auth_ms_new\docker\specs"
PORTAL_SPECS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "public", "specs")

SERVICES = [
    "identity-service", "profile-service", "tenant-service", "session-service",
    "mfa-service", "oauth-service", "wallet-service", "point-service",
    "audit-service", "notification-service", "communication-service",
    "storage-service", "billing-service", "compliance-service", "status-service",
    "secret-service", "saml-service", "pay-service", "thirdparty-service",
    "verification-service", "rbac-service", "gateway-service",
]

# Display names used across the .cn portals (nav, page titles, spec titles).
TITLES = {
    "identity-service": "身份服务",
    "profile-service": "用户资料服务",
    "tenant-service": "租户服务",
    "session-service": "会话服务",
    "mfa-service": "多因素认证服务",
    "oauth-service": "OAuth 服务",
    "wallet-service": "钱包服务",
    "point-service": "积分服务",
    "audit-service": "审计服务",
    "notification-service": "通知服务",
    "communication-service": "通信服务",
    "storage-service": "存储服务",
    "billing-service": "计费服务",
    "compliance-service": "合规服务",
    "status-service": "状态服务",
    "secret-service": "密钥服务",
    "saml-service": "SAML 服务",
    "pay-service": "支付服务",
    "thirdparty-service": "第三方服务",
    "verification-service": "身份验证服务",
    "rbac-service": "RBAC 服务",
    "gateway-service": "网关服务",
}


def main() -> int:
    if not os.path.isdir(SPECS_SRC):
        print(f"ERROR: source not found: {SPECS_SRC}")
        return 1

    os.makedirs(PORTAL_SPECS, exist_ok=True)

    written, removed = 0, 0
    for svc in SERVICES:
        src = os.path.join(SPECS_SRC, svc, "swagger.json")
        if not os.path.isfile(src):
            print(f"  [WARN] missing source spec: {svc}")
            continue

        with open(src, encoding="utf-8") as fh:
            spec = json.load(fh)

        spec.setdefault("info", {})["title"] = f"{TITLES[svc]} API"

        dst = os.path.join(PORTAL_SPECS, f"{svc}.json")
        with open(dst, "w", encoding="utf-8", newline="") as fh:
            json.dump(spec, fh, ensure_ascii=False, indent=2)
        written += 1

    for name in os.listdir(PORTAL_SPECS):
        if name.endswith("-en.json"):
            os.remove(os.path.join(PORTAL_SPECS, name))
            removed += 1

    print(f"wrote {written} Chinese specs, removed {removed} English specs -> {PORTAL_SPECS}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
