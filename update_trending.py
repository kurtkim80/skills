#!/usr/bin/env python3
"""
GitHub Trending Topics & High-Star Agent Skills Auto-Updater
GitHub API를 조회하여 실시간으로 가장 인기 있는 AI 에이전트, 스킬, MCP 저장소를
data/trending.json 및 BlazorHub/wwwroot/data/trending.json에 갱신합니다.
"""

import json
import os
import ssl
import sys
import urllib.parse
import urllib.request
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def update_trending():
    print("🔥 GitHub 최신 인기 AI 에이전트/스킬 테마 수집 시작...")
    ctx = ssl._create_unverified_context()
    headers = {
        'User-Agent': 'Blazor-WASM-SkillHub',
        'Accept': 'application/vnd.github.v3+json'
    }

    # 토큰이 환경 변수에 있으면 추가하여 레이트 리밋 확장
    token = os.environ.get('GITHUB_TOKEN')
    if token:
        headers['Authorization'] = f'token {token}'

    queries = [
        ('topic:mcp sort:stars', '🔌'),
        ('topic:ai-agents sort:stars', '🤖'),
        ('skills in:name,description sort:stars', '⚡'),
        ('reverse engineering sort:stars', '🔍')
    ]

    seen_repos = set()
    themes = []

    # 기본 인기 테마 (Fallback / 우선순위)
    curated = [
        {
            'id': 'morluto-rea',
            'title': '🔍 REA 역공학',
            'query': 'reverse-engineer-anything',
            'repoFullName': 'morluto/rea',
            'stars': 316030,
            'description': 'Reverse engineer anything with agents, from app behavior down to native binaries.',
            'badge': '🔥'
        },
        {
            'id': 'obra-superpowers',
            'title': '⚡ Superpowers',
            'query': 'superpowers',
            'repoFullName': 'obra/superpowers',
            'stars': 301457,
            'description': 'An agentic skills framework & software development methodology that works.',
            'badge': '🔥'
        },
        {
            'id': 'browser-use',
            'title': '🌐 Browser-Use',
            'query': 'browser-use web automation',
            'repoFullName': 'browser-use/browser-use',
            'stars': 61200,
            'description': 'Make websites accessible for AI agents with autonomous browser control.',
            'badge': '🚀'
        },
        {
            'id': 'claude-code',
            'title': '🤖 Claude Code',
            'query': 'claude-code terminal agent',
            'repoFullName': 'anthropics/claude-code',
            'stars': 48500,
            'description': 'Terminal-native agentic coding tool for natural language git and code workflows.',
            'badge': '🌟'
        },
        {
            'id': 'mcp-servers',
            'title': '🔌 MCP 서버',
            'query': 'modelcontextprotocol servers',
            'repoFullName': 'modelcontextprotocol/servers',
            'stars': 64200,
            'description': 'Model Context Protocol official reference servers & tools collection.',
            'badge': '🛠️'
        },
        {
            'id': 'deepseek-r1',
            'title': '🧠 DeepSeek R1',
            'query': 'deepseek r1 reasoning',
            'repoFullName': 'deepseek-ai/DeepSeek-R1',
            'stars': 89200,
            'description': 'DeepSeek reasoning model agents, prompts, and orchestration.',
            'badge': '💡'
        },
        {
            'id': 'openhands',
            'title': '💻 OpenHands',
            'query': 'openhands autonomous coder',
            'repoFullName': 'OpenHands/OpenHands',
            'stars': 45100,
            'description': 'Open-source platform for autonomous software development agents.',
            'badge': '🦾'
        },
        {
            'id': 'claude-context',
            'title': '🎯 RAG & 시맨틱 검색',
            'query': 'claude-context vector search',
            'repoFullName': 'zilliztech/claude-context',
            'stars': 28500,
            'description': 'High-performance codebase vector search MCP server.',
            'badge': '🔍'
        }
    ]

    for c in curated:
        seen_repos.add(c['repoFullName'].lower())
        themes.append(c)

    for q, emoji in queries:
        url = f'https://api.github.com/search/repositories?q={urllib.parse.quote(q)}&order=desc&per_page=6'
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req, context=ctx) as r:
                data = json.loads(r.read().decode())
                for it in data.get('items', []):
                    full_name = it['full_name']
                    stars = it.get('stargazers_count', 0)
                    if full_name.lower() in seen_repos:
                        for t in themes:
                            if t['repoFullName'].lower() == full_name.lower():
                                t['stars'] = stars
                        continue
                    seen_repos.add(full_name.lower())
                    name = it['name']
                    desc = it.get('description') or ''
                    short_title = name.replace('-', ' ').title()
                    if len(short_title) > 22:
                        short_title = short_title[:20] + '…'
                    themes.append({
                        'id': full_name.replace('/', '-').lower(),
                        'title': f'{emoji} {short_title}',
                        'query': name,
                        'repoFullName': full_name,
                        'stars': stars,
                        'description': desc,
                        'badge': '🔥'
                    })
        except Exception as e:
            print(f"⚠️ Query '{q}' 실패 (오프라인/제한): {e}")

    # 스타 수 기준 내림차순 정렬
    themes.sort(key=lambda x: x.get('stars', 0), reverse=True)
    themes = themes[:16]

    out_paths = [
        BASE_DIR / 'data' / 'trending.json',
        BASE_DIR / 'BlazorHub' / 'wwwroot' / 'data' / 'trending.json'
    ]

    for p in out_paths:
        p.parent.mkdir(parents=True, exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            json.dump(themes, f, indent=2, ensure_ascii=False)

    print(f"✅ 총 {len(themes)}개의 최신 인기 테마 갱신 완료!")
    for idx, t in enumerate(themes, 1):
        print(f"  [{idx:02d}] {t['title']} ({t['repoFullName']}) - {t['stars']:,}★")

if __name__ == '__main__':
    update_trending()
