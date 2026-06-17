import os
import re

base_imports = """import discord
from discord.ext import commands
import os, sys, subprocess, textwrap, io, contextlib, asyncio, json, random, datetime, aiohttp, re, base64, string
from collections import Counter
import pyfiglet
"""

def process_code(code):
    # Remove imports
    code = re.sub(r'^(import|from)\s+.*$', '', code, flags=re.MULTILINE)
    # Remove setup function block
    code = re.sub(r'^async def setup\(bot.*?$.*', '', code, flags=re.MULTILINE | re.DOTALL)
    # Remove empty lines
    code = re.sub(r'\n\s*\n', '\n\n', code)
    return code.strip()

with open('cmds.py', 'w', encoding='utf-8') as out:
    out.write(base_imports + "\n\n")
    
    old_dir = 'old_cmds_folder'
    for file in os.listdir(old_dir):
        if file.endswith('.py') and file != '__init__.py':
            out.write(f"# {'='*40}\n# {file}\n# {'='*40}\n")
            with open(os.path.join(old_dir, file), 'r', encoding='utf-8') as f:
                out.write(process_code(f.read()))
            out.write("\n\n")
            
    # Extended features
    out.write(f"# {'='*40}\n# EXTENDED FEATURES\n# {'='*40}\n")
    with open('extented_features.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        
    blocks = re.split(r'# ={60}\n# cogs/(\w+\.py)\n# ={60}', content)
    for i in range(1, len(blocks), 2):
        filename = blocks[i]
        code = blocks[i+1]
        out.write(f"# {'='*40}\n# {filename}\n# {'='*40}\n")
        out.write(process_code(code))
        out.write("\n\n")

# Append the final setup function
with open('cmds.py', 'r', encoding='utf-8') as f:
    full_code = f.read()

class_names = re.findall(r'^class\s+(\w+)\(commands\.Cog', full_code, re.MULTILINE)

with open('cmds.py', 'a', encoding='utf-8') as out:
    out.write("async def setup(bot: commands.Bot):\n")
    for c in class_names:
        out.write(f"    await bot.add_cog({c}(bot))\n")
    
print(f"Generated cmds.py with {len(class_names)} cogs.")
