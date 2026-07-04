#!/usr/bin/env python3
"""Create or promote a Gift AI administrator account."""

from __future__ import annotations

import argparse
import getpass
import sys

from app.core.security import hash_password
from app.database.session import Base, SessionLocal, engine
from app.models.user import User
from app.services.user_service import get_user_by_username


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a new administrator or promote an existing user.",
    )
    parser.add_argument("username", help="Administrator username")
    parser.add_argument(
        "--password",
        help="Password for a new administrator account",
    )
    parser.add_argument(
        "--promote-only",
        action="store_true",
        help="Promote an existing user to administrator without changing the password",
    )
    parser.add_argument(
        "--nickname",
        default="管理员",
        help="Nickname for a newly created administrator",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        existing = get_user_by_username(db, args.username)

        if args.promote_only:
            if existing is None:
                print(f"User not found: {args.username}", file=sys.stderr)
                return 1
            if existing.is_admin:
                print(f"User already admin: {args.username}")
                return 0
            existing.is_admin = True
            db.commit()
            print(f"Promoted to admin: {args.username}")
            return 0

        if existing is not None:
            print(
                f"User already exists: {args.username}. "
                "Use --promote-only to grant admin access.",
                file=sys.stderr,
            )
            return 1

        password = args.password or getpass.getpass("Admin password: ")
        confirm = getpass.getpass("Confirm password: ")
        if password != confirm:
            print("Passwords do not match.", file=sys.stderr)
            return 1
        if len(password) < 8:
            print("Password must be at least 8 characters.", file=sys.stderr)
            return 1

        user = User(
            username=args.username,
            password_hash=hash_password(password),
            nickname=args.nickname,
            is_active=True,
            is_admin=True,
        )
        db.add(user)
        db.commit()
        print(f"Created administrator: {args.username}")
        return 0
    finally:
        db.close()


if __name__ == "__main__":
    raise SystemExit(main())
