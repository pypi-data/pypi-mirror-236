from flask import Blueprint, request
from werkzeug import security
import os
import random
from neoDNS.db import get_db

bp = Blueprint("main", __name__)

try:
    MANAGE_PASSWORD = os.environ['MANAGE_PASSWORD']
except KeyError:
    MANAGE_PASSWORD = None


def get_random_ip(seed) -> str:
    random.seed(seed)
    random_ip = ".".join(map(str, (random.randint(0, 255)
                         for _ in range(4))))
    return random_ip


def get_password_hash(domain_id) -> str:
    db = get_db()

    password_hash = db.execute(
        "SELECT password_hash FROM domains WHERE id == ?",
        domain_id).fetchone()

    if not password_hash:
        return ""
    password_hash = password_hash[0]
    return password_hash


@bp.route("/")
def get_domains():
    db = get_db()
    domains = db.execute("SELECT id, domain from domains").fetchall()

    ans = ""
    for row in domains:
        ans += f"id: {row[0]}, name: {row[1]}<br>"

    print(ans)

    return ans


@bp.route("/get/")
def get_ip():
    domain_id = request.args.get("domain_id")
    password = request.args.get("password")
    if not (domain_id and password):
        return get_random_ip(domain_id)

    password_hash = get_password_hash(domain_id)

    if security.check_password_hash(password_hash, password):
        db = get_db()
        ip = db.execute(
            "SELECT ip FROM domains WHERE id == ?", domain_id).fetchone()
        ip = ip[0]
        return ip
    else:
        return get_random_ip(domain_id)


@bp.route("/add")
def add_address():
    domain = request.args.get("domain_name")
    ip = request.args.get("ip")
    password = request.args.get("password")
    manage_password = request.args.get("manage_password")

    if not (domain and ip and password and manage_password):
        return "ais4Ab6E"

    if not MANAGE_PASSWORD:
        return "Nope"

    if MANAGE_PASSWORD != manage_password:
        return "Eeng8iTh"

    db = get_db()
    db.execute("INSERT INTO domains (domain, ip, password_hash) VALUES (?, ?, ?)",
                 (domain, ip, security.generate_password_hash(password)))
    db.commit()

    return "OK"


@bp.route("/set/")
def set_ip():
    domain_id = request.args.get("domain_id")
    password = request.args.get("password")
    new_ip = request.args.get("new_ip")
    new_pass = request.args.get("new_pass")

    if not (domain_id and password):
        return "bo8ieZaz"

    password_hash = get_password_hash(domain_id)

    if not security.check_password_hash(password_hash, password):
        return "No"

    db = get_db()
    if new_ip:
        db.execute(
            "UPDATE domains SET ip = ? WHERE id = ?", (new_ip, domain_id))
    if new_pass:
        db.execute(
            "UPDATE domains SET password_hash = ? WHERE id = ?",
            (security.generate_password_hash(new_pass), domain_id)
        )
    db.commit()

    return "OK"
