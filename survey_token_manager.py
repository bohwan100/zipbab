#!/usr/bin/env python3
"""
집밥봇 1회용 설문조사 초대 토큰 관리 모듈
- 1회용 고유 토큰 발급 (UUID 기반 8자리 영문/숫자 코드)
- 1회 사용 시 즉시 'used' 처리 및 고객 ID/포털 URL 바인딩
- 재접속/재제출 원천 차단 및 기존 생성 포털로 자동 리다이렉트 지원
"""

import os
import json
import time
import secrets
import string

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(DIRECTORY, "data")
TOKENS_FILE = os.path.join(DATA_DIR, "survey_tokens.json")

os.makedirs(DATA_DIR, exist_ok=True)

def _load_tokens():
    if not os.path.exists(TOKENS_FILE):
        return {}
    try:
        with open(TOKENS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

def _save_tokens(tokens):
    try:
        with open(TOKENS_FILE, "w", encoding="utf-8") as f:
            json.dump(tokens, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"[TokenManager] Error saving tokens: {e}")
        return False

def generate_token(note=""):
    """새로운 8자리 1회용 초대 코드 생성 (예: ZPB-8K2M9X)"""
    tokens = _load_tokens()
    chars = string.ascii_uppercase + string.digits
    # 혼동하기 쉬운 문자(0, O, 1, I) 제외
    clean_chars = "".join([c for c in chars if c not in "0O1I"])
    
    for _ in range(10):
        code = "ZPB-" + "".join(secrets.choice(clean_chars) for _ in range(6))
        if code not in tokens:
            tokens[code] = {
                "token": code,
                "status": "unused",  # "unused" | "used"
                "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "note": note or "1회용 맞춤 식단 초대장",
                "client_id": None,
                "client_name": None,
                "portal_url": None,
                "used_at": None
            }
            _save_tokens(tokens)
            return tokens[code]
    return None

def verify_token(token):
    """
    토큰 유효성 검증
    반환:
      {"status": "valid", "token": token, "data": ...} -> 사용 가능한 1회용 토큰
      {"status": "already_used", "client_id": ..., "portal_url": ...} -> 이미 작성 완료됨
      {"status": "invalid"} -> 존재하지 않거나 유효하지 않은 토큰
    """
    if not token:
        return {"status": "missing", "message": "토큰이 제공되지 않았습니다."}
    
    token = str(token).strip().upper()
    tokens = _load_tokens()
    
    if token not in tokens:
        return {"status": "invalid", "message": "유효하지 않은 초대 코드입니다."}
    
    info = tokens[token]
    if info.get("status") == "used":
        return {
            "status": "already_used",
            "message": "이미 설문 작성이 완료된 1회용 링크입니다.",
            "client_id": info.get("client_id"),
            "client_name": info.get("client_name"),
            "portal_url": info.get("portal_url"),
            "used_at": info.get("used_at")
        }
    
    return {
        "status": "valid",
        "token": token,
        "note": info.get("note", ""),
        "created_at": info.get("created_at")
    }

def mark_token_used(token, client_id, client_name, portal_url):
    """설문 제출 완료 시 토큰을 'used'로 변경하고 고객 포털 정보 바인딩"""
    if not token:
        return False
    token = str(token).strip().upper()
    tokens = _load_tokens()
    
    if token in tokens:
        tokens[token]["status"] = "used"
        tokens[token]["client_id"] = client_id
        tokens[token]["client_name"] = client_name
        tokens[token]["portal_url"] = portal_url
        tokens[token]["used_at"] = time.strftime("%Y-%m-%d %H:%M:%S")
        _save_tokens(tokens)
        print(f"[TokenManager] Token [{token}] marked as USED by [{client_id}].")
        return True
    return False

def get_all_tokens():
    """모든 토큰 목록 최신순 반환"""
    tokens = _load_tokens()
    items = list(tokens.values())
    items.sort(key=lambda x: x.get("created_at", ""), reverse=True)
    return items

def delete_token(token):
    """토큰 삭제"""
    token = str(token).strip().upper()
    tokens = _load_tokens()
    if token in tokens:
        del tokens[token]
        _save_tokens(tokens)
        return True
    return False
