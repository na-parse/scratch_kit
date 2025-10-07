#!/usr/bin/env python3
from pathlib import Path
import os, json

LANCACHE_FQDN = 'azure-cache.unit03.net'
DNSMASQ_FILENAME = Path('00-lancache.dnsmasq')
CACHE_DOMAINS_GIT = 'https://github.com/uklans/cache-domains.git'
CACHE_DIR = Path('./cache-domains')
INCLUDE_CACHE_DOMAINS = [
  "arenanet",  "blizzard",  "bsg",
  "cod",  "daybreak",  "epicgames",
  "origin",  "pathofexile",  "renegadex",
  "riot",  "rockstar",  "sony",
  "square",  "steam",  "uplay",
  "warframe",  "wargaming",  "wsus",
  "xboxlive"
]

def die(msg: str) -> None:
    print(msg)
    exit(1)

def vardump(thisObj):
    print(json.dumps(thisObj,indent=2))

def get_cache_domains_conf(cache_dir: Path) -> list:
    # Requires a clone of uklans/cache-domains in current directory
    if not cache_dir.is_dir(): die(f'Clone of {CACHE_DOMAINS_GIT} is required.')
    cache_domains_json = Path(cache_dir / 'cache_domains.json')
    if not cache_domains_json.is_file():
        die(f'Unable to find cache_domains.json in ./cache-domains')
    
    with open(cache_domains_json,'r') as f:
        return json.load(f)['cache_domains']

def generate_dnsmasq(list_of_fqdns) -> list:
    ''' Outputs the final DNSMASQ config file for lancache forwarding '''
    print(
        f'### 00-lancache - DNSMASQ config file for CNAME redirects to LANCACHE\n'
        f'### Server {LANCACHE_FQDN} based on uklans/cache-domains.git'
    )
    lines =  []
    for fqdn in list_of_fqdns:
        if fqdn.startswith('# - '):
            # Comment line to indicate source of following records
            lines.append(f'\n{fqdn}')
        else:
            lines.append(f'cname={fqdn},{LANCACHE_FQDN}')
    return lines

def output_dnsmasq(lines):
    with open(DNSMASQ_FILENAME,'w') as f:
        _ = f.write("\n".join(lines) + '\n')
    print("\n".join(lines))


def main() -> None:
    cache_domains = get_cache_domains_conf(CACHE_DIR)
    use_files = [ 
        x for y in cache_domains
        if y['name'] in INCLUDE_CACHE_DOMAINS
        for x in y['domain_files']
    ]
    fqdns = []
    for use_file in use_files:
        cache_file = CACHE_DIR / use_file
        fqdns += [ f'# - {str(cache_file)}' ]
        with open(cache_file,'r') as f:
            fqdns += [ x.strip() for x in f.readlines() ]
    dnsmasq_lines = generate_dnsmasq(fqdns)
    output_dnsmasq(dnsmasq_lines)

    print(f'\n\n==========\n\n')
    print(f'- updated dnsmasq file available as {str(DNSMASQ_FILENAME)}')
    print(f'- install on pi.hole as /etc/dnsmasq.d/{str(DNSMASQ_FILENAME)}')

if __name__ == '__main__':
    main()