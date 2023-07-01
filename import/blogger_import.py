#! /usr/bin/env python3
import atoma
import os
import sys
import attr
from datetime import datetime
from markdownify import markdownify as md


FILENAME = "/Users/blaise/Downloads/blog-06-30-2023.xml"
TAG="touring"
DRY=False
feed = atoma.parse_atom_file(FILENAME)
entries = feed.entries

@attr.s
class MdPosts:
    title: str = attr.ib()
    date: datetime = attr.ib()
    content: str = attr.ib()

md_posts = []
print(entries[53])
print(entries[-1])
for entry in entries:
    if 'http://schemas.google.com/blogger/2008/kind#post' not in [cat.term for cat in entry.categories]:
        print("Skipping id", entry.id_)
        continue
    print("Handling id", entry.id_)
    md_posts.append(MdPosts(entry.title.value, entry.published if entry.published else entry.updated, entry.content.value))
print(md_posts[-1])
print(f"Found {len(md_posts)} posts")

directory = "converted"
if not DRY:
    os.makedirs(directory, exist_ok=True)
for post in md_posts:
    simple_title = post.title.lower()
    simple_title = simple_title.translate(str.maketrans(' \t', '__', '?![]{}-_()*&^%$#@!:;<>,./'))
    post_datestr = f"{post.date.year}-{post.date.month}-{post.date.day}"
    post_filename= f"{post_datestr}-{simple_title}.md"
    print("Handling", post_filename)
    if not DRY:
        outfile = os.path.join(directory, post_filename)
        with open(outfile, "w") as f:
            f.write((
f"""---
layout: post
title:  "{post.title}"
date: {post.date.isoformat(' ', 'seconds')}
categories: {TAG}
---
{md(post.content)}
"""))

