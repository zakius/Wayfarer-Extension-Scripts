#!/usr/bin/env python3
"""main build script."""

import argparse
import configparser
import re
from pathlib import Path

def readtext(filename):
  return filename.read_text(encoding='utf-8-sig')

def fill_meta(source, script_name):
  meta = ['// ==UserScript==']
  keys = set()

  def append_line(key, value):
    if key not in keys:
      meta.append(f'// @{key:<14} {value}')

  for line in source.splitlines():
    text = line.lstrip()
    rem = text[:2]
    if rem != '//':
      raise UserWarning(f'{script_name}: wrong line in metablock: {line}')
    text = text[2:].strip()
    try:
      key, value = text.split(None, 1)
    except ValueError:
      if text == '==UserScript==':
        # raise UserWarning(f'{script_name}: wrong metablock detected')
        continue
      elif text == '==/UserScript==':
        # raise UserWarning(f'{script_name}: wrong metablock detected')
        continue
    else:
      if key[0] == '@':
        key = key[1:]
      else:  # continue previous line
        meta[-1] += ' ' + text
        continue

      if key == 'version':
        sversion = value
        if not re.match(r'^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$', value):
          print(f'{script_name}: wrong version format: {value}')  # expected: major.minor.patch
      elif key == 'name':
          sname = value 
          line = line.replace(value, 'WFES - ' + value)
      elif key == 'description':
        sdescription = value 

      append_line(key,value)

  append_line('namespace', cfg['namespace'])

  url_dist_base = cfg.get('url_dist_base',fallback = False)
  if url_dist_base:
    path = url_dist_base + script_name
    append_line('updateURL', path + '.meta.js')
    append_line('downloadURL', path + '.user.js')
    surl = path + '.user.js'

  if keys.isdisjoint({'match', 'include'}):
    append_line('match', cfg['match'])

  append_line('icon', 'https://wayfarer.nianticlabs.com/imgpub/favicon-256.png')
  append_line('supportURL', 'https://github.com/AlterTobi/WFES/issues')
  append_line('grant', 'none')
  meta.append('// ==/UserScript==\n')
  
  sl = '  * [{}]({}) {}\n    - {}\n'.format(sname,surl,sversion,sdescription)
  return '\n'.join(meta), sl

def process_file(source, out_dir):
  """Generate .user.js and .meta.js from given source file.

    Resulted file(s) put into out_dir (if specified, otherwise - use current).
    """
  try:
    meta, script = readtext(source).split('\n\n', 1)
  except ValueError:
    raise Exception(f'{source}: wrong input: empty line expected after metablock')

  script_name = source.stem
  
  meta, shortl = fill_meta(meta, script_name)
  
  data = [
    meta,
    script
    ]

  (out_dir / (script_name + '.user.js')).write_text(''.join(data), encoding='utf8')
  (out_dir / (script_name + '.meta.js')).write_text(meta, encoding='utf8')
  return shortl

def run():
  source = Path('..')
  target = Path('../build')
  target.mkdir(parents=True,exist_ok = True)
  # copy md files
  all_files = source.glob('*.md')
  for file in all_files:
    print('process file {} {}'.format(file,target))
    tf = target / file.name
    file.link_to(tf)
    
  # process js files
  shortlist = []
  shortlist.append('## shortlist\n\n')
  shortlist.append('created automatically\n\n')
  shortlist.append('Not all scripts on this page are fully functional. This list is for reference only. Use at your own risk.\n\n')
  
  all_files = list(source.glob('**/*.js'))
  for filename in all_files:
    print('process file {} {}'.format(filename,target))
    short = process_file(
      filename,
      target
      )
    shortlist.append(short)

  shortdest = target / 'shortlist.md'
  shortdest.write_text(''.join(shortlist), encoding='utf8')

##### MAIN ######

if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('--config_file', '-c', help='config file', default='build.ini')
  args = parser.parse_args()
  
  config = configparser.ConfigParser()
  config.read(args.config_file)
  cfg = config['defaults']
  run()
  
