# Migration Guide: Cleaning Up Old Code

## Overview

Your project has evolved from a prototype with scattered modules to a professional FastAPI structure. This guide explains what to do with the old root-level files.

---

## 📊 Old Files Inventory

| File | Size | Status | New Location | Action |
|------|------|--------|--------------|--------|
| `behaviour.py` | ~0 bytes | Empty | N/A | ✅ **DELETE** |
| `llm.py` | ~0 bytes | Empty | N/A | ✅ **DELETE** |
| `main.py` | ~250 bytes | Deprecated | → `app/main.py` | ✅ **DELETE** |
| `modes.py` | ~150 bytes | **MIGRATED** | → `app/schemas/chat.py` | ✅ **DELETE** |
| `prompts.py` | ~400 bytes | **MIGRATED** | → `app/utils/prompts.py` | ✅ **DELETE** |
| `safety.py` | ~300 bytes | **MIGRATED** | → `app/utils/safety.py` | ✅ **DELETE** |
| `schemas.py` | ~200 bytes | **MIGRATED** | → `app/schemas/chat.py` | ✅ **DELETE** |

**Total:** ~1.3 KB of deprecated code that should be removed.

---

## ✅ Checklist: Before You Delete

- [ ] Read this guide completely
- [ ] Back up your project (git commit or copy folder)
- [ ] Verify new code is working:
  ```bash
  pytest
  uvicorn app.main:app --reload
  ```
- [ ] Check that you're not importing from old files anywhere
- [ ] Confirm git status is clean or committed

---

## 🗑️ Deletion Methods

### Method 1: Windows PowerShell (Recommended)

**Safe - with confirmation:**
```powershell
cd c:\Users\AAGATI\Downloads\ai chatbot\ai chatbot

# Delete individually (you approve each one)
Remove-Item behaviour.py -Confirm
Remove-Item llm.py -Confirm
Remove-Item main.py -Confirm
Remove-Item modes.py -Confirm
Remove-Item prompts.py -Confirm
Remove-Item safety.py -Confirm
Remove-Item schemas.py -Confirm
```

**Fast - all at once:**
```powershell
cd c:\Users\AAGATI\Downloads\ai chatbot\ai chatbot
Remove-Item @('behaviour.py', 'llm.py', 'main.py', 'modes.py', 'prompts.py', 'safety.py', 'schemas.py') -Force
```

### Method 2: Windows Command Prompt

```cmd
cd c:\Users\AAGATI\Downloads\ai chatbot\ai chatbot
del behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py
```

### Method 3: macOS/Linux Terminal

**Safe - with confirmation:**
```bash
cd ~/path/to/ai-chatbot
rm -i behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py
```

**Fast - all at once:**
```bash
cd ~/path/to/ai-chatbot
rm behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py
```

### Method 4: Using Git (If Version Controlled)

This tracks deletions for commit:
```bash
cd ~/path/to/ai-chatbot
git rm behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py
git commit -m "Remove deprecated root-level modules - migrated to app/ package"
git push
```

### Method 5: Safer - Create Archive First

**Windows:**
```powershell
# Create backup folder
mkdir old_code_backup

# Move files instead of deleting
Move-Item @('behaviour.py', 'llm.py', 'main.py', 'modes.py', 'prompts.py', 'safety.py', 'schemas.py') -Destination old_code_backup/

# You can now delete old_code_backup/ later if desired
```

**macOS/Linux:**
```bash
# Create backup folder
mkdir old_code_backup

# Move files instead of deleting
mv behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py old_code_backup/

# You can now delete old_code_backup/ later if desired
```

---

## 📝 Code Migration Reference

### Import Path Changes

If you find any remaining code importing from old modules, here's the mapping:

**Old Import → New Import**

```python
# Old (Don't Use)
from modes import Mode

# New (Use This)
from app.schemas.chat import ModeEnum
```

```python
# Old (Don't Use)
from prompts import get_system_prompt

# New (Use This)
from app.utils.prompts import get_system_prompt
```

```python
# Old (Don't Use)
from safety import safety_check

# New (Use This)
from app.utils.safety import safety_check, detect_crisis_keywords, get_crisis_response
```

```python
# Old (Don't Use)
from schemas import ChatRequest, ChatResponse

# New (Use This)
from app.schemas.chat import ChatRequest, ChatResponse, ModeEnum
```

---

## 🔍 Verify After Deletion

After deleting the old files, run these checks:

### 1. Syntax & Import Check
```bash
python -c "from app.main import app; print('✓ Imports work correctly')"
```

Expected output:
```
✓ Imports work correctly
```

### 2. Run Tests
```bash
pytest -v
```

All tests should pass.

### 3. Start Server
```bash
uvicorn app.main:app --reload
```

Should start without errors.

### 4. Test an Endpoint
```bash
curl http://localhost:8000/health
```

Should return:
```json
{"status":"healthy","app":"Therapeutic AI Chatbot","version":"0.1.0"}
```

### 5. Check File Listing
```bash
# Windows PowerShell
Get-ChildItem -Name | findstr "\.py$" | findstr -v "app"

# macOS/Linux
ls -la | grep "\.py$"
```

Should NOT show any of the old files.

---

## 🔄 If Something Goes Wrong

### "ImportError: cannot import name X"

**Problem:** Code still trying to import from old modules.

**Solution:**
```bash
# Search for old imports
grep -r "from modes import" .
grep -r "from prompts import" .
grep -r "from safety import" .
grep -r "from schemas import" .
```

Update those import statements to use new paths from above.

### "File not found" when starting app

**Problem:** Code reference to deleted files still exists.

**Solution:**
1. Check the error message for filename
2. Search codebase: `grep -r "behaviour.py" .` (or other filename)
3. Fix the import or file reference
4. Try again

### Server won't start after deletion

**Problem:** Unexplained startup failure.

**Solution:**
```bash
# Restore from backup if you created one
# Or git checkout if you haven't committed yet
git checkout behaviour.py llm.py main.py modes.py prompts.py safety.py schemas.py

# Then run tests
pytest
```

---

## 🎯 Why These Files Matter

### `modes.py` → `app/schemas/chat.py`
- **Old:** Simple enum with 4 modes
- **New:** ModeEnum in professional schema module with type validation

### `prompts.py` → `app/utils/prompts.py`
- **Old:** Single function `get_system_prompt()`
- **New:** Multiple functions for different therapeutic needs:
  - `get_system_prompt()` - Original function
  - `get_safety_prompt()` - New safety system
  - `get_modes_description()` - New helper

### `safety.py` → `app/utils/safety.py`
- **Old:** Single function `safety_check()`
- **New:** Enhanced safety module:
  - `detect_crisis_keywords()` - Improved detection
  - `get_crisis_response()` - Categorized responses
  - `is_safety_violation()` - Comprehensive checking

### `schemas.py` → `app/schemas/chat.py`
- **Old:** Basic data classes
- **New:** Professional Pydantic models with:
  - Full validation
  - Type hints
  - Documentation
  - Config requirements

### `main.py` → `app/main.py`
- **Old:** Single placeholder endpoint
- **New:** Complete FastAPI application with:
  - 11 professional endpoints
  - Database integration
  - Middleware setup
  - Error handling
  - Health checks

---

## 📚 After Cleanup

Once deleted, you'll have:
- ✅ Cleaner root directory
- ✅ No duplicate code
- ✅ Single source of truth (app/ package)
- ✅ Professional project structure
- ✅ No import confusion
- ✅ Ready for production

---

## 🎓 What You Get

The new `app/` structure provides:

1. **Better Organization**
   - Models in `app/models/`
   - Schemas in `app/schemas/`
   - Routes in `app/routes/`
   - Business logic in `app/services/`
   - Utilities in `app/utils/`

2. **Enhanced Features**
   - More comprehensive safety checks
   - Better error handling
   - Professional data validation
   - Database integration
   - Authentication scaffolding

3. **Production Ready**
   - Security best practices
   - Logging configured
   - Type hints throughout
   - Error handling
   - Test infrastructure

---

## 🚀 Next Steps

1. **Delete** the old files using one of the methods above
2. **Verify** using the checklist in [Verify After Deletion](#-verify-after-deletion)
3. **Test** by running the application and API
4. **Commit** to git: `git commit -m "Remove deprecated root-level code"`
5. **Continue** developing new features!

---

## ❓ FAQ

### Q: Can I keep the old files as backup?
**A:** Not recommended - they're not used and create confusion. If you want a backup, use git history or create `old_code_backup/` folder.

### Q: Do I need to update any code?
**A:** Only if you have custom code importing from old modules. Check with:
```bash
grep -r "from modes\|from prompts\|from safety\|from schemas" app/ tests/
```

### Q: What if I'm not sure about deletion?
**A:** Create a git commit first, then delete. You can always revert:
```bash
git reset --hard HEAD~1
```

### Q: How do I know if everything works after deletion?
**A:** Run this sequence:
```bash
pytest
python -c "from app.main import app; print('✓')"
uvicorn app.main:app --reload
curl http://localhost:8000/health
```

All should work without errors.

---

## 📞 Need Help?

- Check [README.md](README.md#-support--issues) support section
- Review test files in `tests/` for usage examples
- Check git history: `git log --oneline`
- Run with verbose output: `python -v`

---

**Status:** Ready to cleanup! ✨

Delete with confidence - your code is safe in the new `app/` package.
