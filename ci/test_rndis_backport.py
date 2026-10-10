#!/usr/bin/env python3
"""Compile and exercise the actual vendor RNDIS parser with host skb stubs."""
import argparse, subprocess, tempfile, os
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('kernel',type=Path);a=p.parse_args()
s=(a.kernel/'drivers/usb/gadget/function/rndis.c').read_text();start=s.index('int rndis_rm_hdr(');end=s.index('EXPORT_SYMBOL_GPL(rndis_rm_hdr)',start)
source=r'''
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <stdio.h>
typedef uint32_t u32;
static u32 get_unaligned_le32(const void *p) {u32 n;memcpy(&n,p,4);return n;}
#define RNDIS_MSG_PACKET 1
#define EINVAL 22
#define EOVERFLOW 75
#define ENOMEM 12
#define GFP_ATOMIC 0
#define le32_to_cpu(x) (x)
#define pr_err(...) ((void)0)
struct gether { int unused; };
struct rndis_packet_msg_type {u32 MessageType,MessageLength,DataOffset,DataLength;u32 rest[7];} __attribute__((packed));
struct sk_buff {unsigned char storage[512];unsigned char *data;unsigned len;};
struct sk_buff_head {struct sk_buff *items[8];unsigned count;};
static struct sk_buff *new_skb(void) {struct sk_buff *s=calloc(1,sizeof(*s));s->data=s->storage;return s;}
static void dev_kfree_skb_any(struct sk_buff *s) {free(s);}
static void skb_pull(struct sk_buff *s,unsigned n) {assert(n<=s->len);s->data+=n;s->len-=n;}
static void skb_trim(struct sk_buff *s,unsigned n) {if(n<s->len)s->len=n;}
static struct sk_buff *skb_clone(struct sk_buff *s,int flags) {struct sk_buff *n=new_skb();memcpy(n->data,s->data,s->len);n->len=s->len;return n;}
static void skb_queue_tail(struct sk_buff_head *q,struct sk_buff *s) {assert(q->count<8);q->items[q->count++]=s;}
'''+s[start:end]+r'''
static void packet(struct sk_buff *s,unsigned char value,unsigned n,unsigned pad) {
 struct rndis_packet_msg_type h={.MessageType=1,.MessageLength=44+n+pad,.DataOffset=36,.DataLength=n};
 memcpy(s->data+s->len,&h,44);memset(s->data+s->len+44,value,n);memset(s->data+s->len+44+n,0,pad);s->len+=h.MessageLength;
}
static void check(unsigned packets,unsigned pad,unsigned extra) {
 struct sk_buff *s=new_skb();struct sk_buff_head q={0};
 for(unsigned i=0;i<packets;i++)packet(s,0x30+i,20+i,pad);
 if(extra)s->data[s->len++]=0;
 assert(rndis_rm_hdr(NULL,s,&q)==0);assert(q.count==packets);
 for(unsigned i=0;i<q.count;i++){assert(q.items[i]->len==20+i);for(unsigned j=0;j<q.items[i]->len;j++)assert(q.items[i]->data[j]==0x30+i);free(q.items[i]);}
}
int main(void) {
 for(unsigned n=1;n<=3;n++)for(unsigned p=0;p<=3;p++)for(unsigned e=0;e<=1;e++)check(n,p,e);
 struct sk_buff *s=new_skb();struct sk_buff_head q={0};s->len=10;assert(rndis_rm_hdr(NULL,s,&q)==-EINVAL);assert(q.count==0);
 puts("25 actual RNDIS parser cases passed");
}
'''
with tempfile.TemporaryDirectory() as tmp:
 d=Path(tmp);(d/'test.c').write_text(source)
 subprocess.run([os.environ.get('UTXPERIA_HOST_CLANG','/usr/bin/clang'),'-fsanitize=address,undefined','-g','-O1',str(d/'test.c'),'-o',str(d/'test')],check=True)
 subprocess.run([str(d/'test')],check=True,env={**os.environ,'ASAN_OPTIONS':'detect_leaks=0','UBSAN_OPTIONS':'halt_on_error=1'})
