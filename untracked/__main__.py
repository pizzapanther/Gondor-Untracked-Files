#!/usr/bin/env python

import os
import re
import sys
import glob
import shutil
import argparse
import ConfigParser

def main():
  parser = argparse.ArgumentParser(description='Update Gondor config with multiple untracked files')
  parser.add_argument('directories', metavar='DIR', nargs='+', help='Directory to recurse')
  parser.add_argument('--config', dest='config', default='.gondor/config', help='Path to config file, Default: .gondor/config')
  parser.add_argument('--configold', dest='configold', default='.gondor/config.old', help='Path to copy old config file, Default: .gondor/config.old')
  parser.add_argument('--exclude', dest='exclude', action='append', default=[], help='Exclude files. Default: *.pyc., .*')
  parser.add_argument('--excludedir', dest='excludedir', action='append', default=[], help='Exclude directories. Default: .git')
  
  args = parser.parse_args()
  
  shutil.copyfile(args.config, args.configold)
  config = ConfigParser.RawConfigParser()
  config.read(args.config)
  
  include_files = []
  
  prefix = os.path.basename(os.getcwd())
  
  exclude = ['*.pyc', '.*']
  if args.exclude:
    exclude = args.exclude
    
  excludedir = ['.git']
  if args.excludedir:
    excludedir = args.excludedir
    
  for d in args.directories:
    for root, dirs, files in os.walk(d):
      skip = False
      for ed in excludedir:
        if re.search(re.escape(ed), root):
          skip = True
          break
          
      if skip:
        continue
        
      else:
        tfiles = [os.path.join(root, f) for f in files]
        bad = []
        for ef in exclude:
          globs = glob.glob(os.path.join(root, ef))
          for f in tfiles:
            if f in globs:
              bad.append(f)
              
        for b in bad:
          tfiles.remove(b)
          
        include_files.extend(tfiles)
        
  include_str = ''
  for f in include_files:
    include_str += os.path.join(prefix, f) + '\n'
    
  include_str = include_str[:-1]
  if not config.has_section('files'):
    config.add_section('files')
    
  config.set('files', 'include', include_str)
  with open(args.config, 'wb') as configfile:
    config.write(configfile)
    