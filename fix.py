import shutil

TARGET_FILE = "fast6.py"
BACKUP_FILE = "fast6_before_auth_fix.py"

print("🔐 FORCE AUTH FIX STARTING...")

# Backup
shutil.copy(TARGET_FILE, BACKUP_FILE)
print(f"✅ Backup saved: {BACKUP_FILE}")

with open(TARGET_FILE, "r", encoding="utf-8") as f:
    code = f.read()

# =========================
# FORCE INSERT CLEAN AUTH BLOCK
# =========================

auth_block = """

# =========================
# 🔐 FIXED AUTH SYSTEM (FORCED)
# =========================

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    print("🔍 Verifying password...")
    print("   Input:", plain_password)
    print("   Stored:", hashed_password)

    try:
        if hashed_password.startswith("$"):
            result = pwd_context.verify(plain_password, hashed_password)
            print("   bcrypt result:", result)
            return result
        else:
            result = plain_password == hashed_password
            print("   plain match:", result)
            return result
    except Exception as e:
        print("❌ Verify error:", e)
        return False


def authenticate_user(db, username, password):
    print(f"🔐 Login attempt: {username}")

    user = db.query(User).filter(User.username == username).first()

    if not user:
        print("❌ USER NOT FOUND")
        return None

    print(f"👤 DB User: {user.username}")
    print(f"🔑 DB Password: {user.password}")

    if not verify_password(password, user.password):
        print("❌ PASSWORD WRONG")
        return None

    print("✅ LOGIN SUCCESS")
    return user


@app.post("/login")
async def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    user = authenticate_user(db, username, password)

    if not user:
        print("❌ LOGIN FAILED")
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Invalid username or password"
        })

    # AUTO FIX PASSWORD (IMPORTANT)
    if not user.password.startswith("$"):
        print("⚠️ Upgrading plain password to bcrypt...")
        user.password = pwd_context.hash(password)
        db.commit()

    access_token = create_access_token(data={"sub": user.username})

    response = RedirectResponse(url="/dashboard", status_code=303)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True
    )

    print("🍪 Cookie set, redirecting...")

    return response


async def get_current_user(request: Request, db: Session = Depends(get_db)):

    token = request.cookies.get("access_token")

    print("🍪 Cookie:", token)

    if not token:
        raise HTTPException(status_code=401, detail="No token")

    if token.startswith("Bearer "):
        token = token.replace("Bearer ", "")

    from jose import jwt

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        print("👤 Token user:", username)
    except Exception as e:
        print("❌ Token decode error:", e)
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.username == username).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

# =========================
# END AUTH FIX
# =========================

"""

# Append at END to override everything
code = code + "\n" + auth_block

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(code)

print("✅ FORCE AUTH PATCH APPLIED")
print("👉 Restart server now:")
print("   uvicorn fast6:app --port 9090")