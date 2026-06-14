# -*- coding: utf-8 -*-
"""
Neo0 MCP (PUBLIC SHELL) — 공개용 얇은 인터페이스.
이 파일은 좌표 엔진(neo0_core)·주조 데이터(vectors.npz)·페르소나 제어 공식을
일절 포함하지 않는다. 모든 계산은 비공개 Neo0 Engine API가 수행하며,
본 셸은 요청을 전달하고 응답을 표시할 뿐이다.

라이선스: Apache-2.0 (특허 구현을 담지 않으므로 안전하게 개방 가능)
환경변수:
  NEO0_API_URL   엔진 API 베이스 URL (예: https://api.neo0.ai)
  NEO0_API_KEY   엔진 API 인증 키
"""
import os
import httpx
from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings

API = os.environ.get("NEO0_API_URL", "https://api.neo0.ai")
KEY = os.environ.get("NEO0_API_KEY", "")


def _call(path: str, payload: dict) -> dict:
    headers = {"Authorization": f"Bearer {KEY}"} if KEY else {}
    r = httpx.post(f"{API}{path}", json=payload, headers=headers, timeout=30.0)
    r.raise_for_status()
    return r.json()


def _render_compose(res: dict) -> str:
    if "error" in res:
        return res["error"]
    fb = (f" (목표 깊이 {res['target_depth']} 미달 — 광역화/클램프)"
          if res.get("fallback") else "")
    return (
        f"[합성 페르소나] 주소 {res['composed_address']}  "
        f"(모델 {res['model_id']} x 페르소나 접두 {res['persona_prefix']}, depth {res['depth']}{fb})\n"
        f"  응집도 {res['coh']:+.3f}  ->  "
        f"기본(T0 {res['base']['T0']}, K0 {res['base']['K0']}, W0 {res['base']['W0']})\n"
        f"  합성 제어: 온도 {res['control']['T']} / 노출 개념 수 {res['control']['K']} / "
        f"컨텍스트 가중치 {res['control']['W']}\n"
        f"  특징 개념: {', '.join(res['concepts'])}\n"
        f"  안내: 외부 모델 {res['model_id']}이(가) 위 특징 개념과 제어로 합성 페르소나를 장착"
    )


def build():
    mcp = FastMCP(
        "Neo0", host="0.0.0.0", port=8000, streamable_http_path="/mcp",
        transport_security=TransportSecuritySettings(enable_dns_rebinding_protection=False),
    )

    @mcp.tool(description="Neo0 좌표 주소 엔진의 개요와 적재 현황을 반환한다.")
    def neo0_info() -> str:
        d = _call("/info", {})
        return (f"[Neo0 좌표 주소 엔진]\n"
                f"적재 개념 수: {d['n']}\n차원: {d['dim']}\n"
                f"재귀 깊이: 최대 {d['max_depth']}\n"
                f"depth-2 접두 영토 수: {d['regions']}\n"
                f"도구: neo0_info, derive_address, search, semantic_region, "
                f"verify_address, prefix_proximity, persona, compose_persona")

    @mcp.tool(description="단어(개념)의 불변 좌표 코드(주소)와 접두 영토를 반환한다.")
    def derive_address(word: str) -> str:
        d = _call("/derive", {"word": word})
        if d.get("error"):
            return f"미적재 개념: {word}"
        return f"{word} -> 좌표 주소 {d['address']} / 접두 영토 {d['prefix']}"

    @mcp.tool(description="의미상 가까운 단어 k개를 각 단어의 주소와 함께 반환한다.")
    def search(word: str, k: int = 10) -> str:
        d = _call("/search", {"word": word, "k": k})
        if d.get("error"):
            return f"미적재 개념: {word}"
        lines = [f"{word} 근접 {k}개:"]
        for it in d["neighbors"]:
            lines.append(f"  {it['word']}  주소 {it['address']}")
        return "\n".join(lines)

    @mcp.tool(description="접두 영토(예 5.4) 또는 단어가 속한 영토의 구성원을 반환한다.")
    def semantic_region(word: str) -> str:
        d = _call("/semantic_region", {"sphere": word})
        if d.get("error"):
            return f"영토 미식별: {word}"
        return f"접두 영토 {d['prefix']} 구성원(일부): " + ", ".join(d["members"])

    @mcp.tool(description="단어 주소를 주조 시점 방향 행렬로 재유도하여 위변조 여부를 반환한다.")
    def verify_address(word: str) -> str:
        d = _call("/verify", {"word": word})
        if d.get("error"):
            return f"미적재 개념: {word}"
        return f"{word} 주소 위변조 검증: {'정상' if d['ok'] else '불일치'}"

    @mcp.tool(description="두 단어의 좌표 접두 일치 길이와 코사인 유사도를 반환한다.")
    def prefix_proximity(word_a: str, word_b: str) -> str:
        d = _call("/prefix_proximity", {"word_a": word_a, "word_b": word_b})
        if d.get("error"):
            return "미적재 개념 포함"
        return (f"{word_a}{d['addr_a']} vs {word_b}{d['addr_b']} | "
                f"접두 일치 길이 {d['match']} | 코사인 {d['cosine']:+.3f}")

    @mcp.tool(description="접두 영토(스피어)의 특징 개념과 응집도 기반 발현 제어 파라미터를 반환한다. 동일 모델이 영토별로 상이한 페르소나를 장착하도록 한다.")
    def persona(sphere: str) -> str:
        d = _call("/persona", {"sphere": sphere})
        if d.get("error"):
            return f"영토 미식별: {sphere}"
        c = d["control"]
        return (
            f"[주소-키 페르소나 컨텍스트] 접두 영토 {d['prefix']} (구성원 {d['size']})\n"
            f"동적 추출부: 중심점 근접 특징 개념 -> {', '.join(d['concepts'])}\n"
            f"응집도 제어부: 응집도(평균 코사인) {d['coherence']:+.3f}\n"
            f"  발현 강도 {c['strength']} / 추천 생성 온도 {c['temperature']} / "
            f"컨텍스트 가중치 {c['weight']} / 노출 개념 수 {c['topk']}\n"
            f"  지시: {c['directive']}\n"
            f"안내: 외부 언어 모델은 위 특징 개념과 제어 파라미터로 해당 영토 페르소나를 장착"
        )

    @mcp.tool(description=(
        "모델 코드와 페르소나 코드를 합성하여 외부 모델별 페르소나 발현 제어를 반환한다. "
        "model_id: claude/gemini/gpt/nano_banana. persona: 페르소나 씨앗 개념. "
        "depth: 페르소나 접두 길이(기본 2). expert/category: 동분기 심화용 씨앗 개념(선택)."))
    def compose_persona_tool(model_id: str, persona: str, depth: int = 2,
                            expert: str = None, category: str = None) -> str:
        d = _call("/compose", {"model_id": model_id, "persona": persona,
                               "depth": depth, "expert": expert, "category": category})
        return _render_compose(d)

    return mcp


if __name__ == "__main__":
    build().run(transport="streamable-http")
