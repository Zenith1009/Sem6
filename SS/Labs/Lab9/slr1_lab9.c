#include <stdio.h>
#include <string.h>
#include <ctype.h>

#define MAXP  12
#define MAXS  64
#define MAXI  128

typedef struct { char lhs; char rhs[8]; int len; } Prod;
Prod P[MAXP]; static int np = 0;

const char NT[] = "\'SBCDEF";  /* '\'' = S' */
#define NN 7
const char TM[] = "abcfgh$";
#define NT_T 7

int ni(char c){ int i; for(i=0;i<NN;i++) if(NT[i]==c) return i; return -1; }
int ti(char c){ int i; for(i=0;i<NT_T;i++) if(TM[i]==c) return i; return -1; }

void prod(char l, const char *r){
    P[np].lhs = l;
    if(r[0]=='#'){ P[np].rhs[0]='#'; P[np].rhs[1]=0; P[np].len=0; }
    else { strncpy(P[np].rhs,r,7); P[np].len=strlen(r); }
    np++;
}

int FIRST[NN][128], FOLLOW[NN][128];

int add(int s[128], char c){ if(!s[(unsigned char)c]){s[(unsigned char)c]=1;return 1;} return 0; }
int merge(int dst[128], int src[128], int skip_eps){
    int c,ch=0;
    for(c=0;c<128;c++) if(src[c]&&!(skip_eps&&c=='#')&&!dst[c]){dst[c]=1;ch=1;}
    return ch;
}

void first_str(const char *s, int out[128]){
    int i, all=1; memset(out,0,128*sizeof(int));
    if(!s||s[0]==0||s[0]=='#'){ out['#']=1; return; }
    for(i=0;s[i];i++){
        char x=s[i]; int idx=ni(x);
        if(idx<0){ add(out,x); all=0; break; }
        merge(out,FIRST[idx],1);
        if(!FIRST[idx]['#']){ all=0; break; }
    }
    if(all) out['#']=1;
}

void compute_first(){
    int ch=1;
    while(ch){ int i; ch=0;
        for(i=0;i<np;i++){
            int f[128]; first_str(P[i].rhs,f);
            if(merge(FIRST[ni(P[i].lhs)],f,0)) ch=1;
        }
    }
}

void compute_follow(){
    add(FOLLOW[ni('\'')],'$'); add(FOLLOW[ni('S')],'$');
    int ch=1;
    while(ch){ int i; ch=0;
        for(i=0;i<np;i++){
            int li=ni(P[i].lhs); const char *r=P[i].rhs; int j,len=strlen(r);
            if(r[0]=='#') continue;
            for(j=0;j<len;j++){
                int bi=ni(r[j]); if(bi<0) continue;
                int fb[128]; first_str(r+j+1,fb);
                if(merge(FOLLOW[bi],fb,1)) ch=1;
                if(fb['#']&&merge(FOLLOW[bi],FOLLOW[li],0)) ch=1;
            }
        }
    }
}

typedef struct { int p, dot; } Item;
typedef struct { Item it[MAXI]; int n; } ISet;

ISet states[MAXS]; static int ns=0;
int GOTO[MAXS][128];  /* goto table (all symbols) */

int has(ISet *s, Item x){ int i; for(i=0;i<s->n;i++) if(s->it[i].p==x.p&&s->it[i].dot==x.dot) return 1; return 0; }
void push(ISet *s, Item x){ if(!has(s,x)) s->it[s->n++]=x; }

void closure(ISet *s){
    int ch=1;
    while(ch){ int i; ch=0;
        for(i=0;i<s->n;i++){
            Prod *p=&P[s->it[i].p]; int dot=s->it[i].dot;
            if(p->rhs[0]=='#'||dot>=p->len) continue;
            char X=p->rhs[dot]; int j;
            if(!isupper((unsigned char)X)&&X!='\'') continue;
            for(j=0;j<np;j++) if(P[j].lhs==X){
                Item it={j,0}; if(!has(s,it)){push(s,it);ch=1;}
            }
        }
    }
}

ISet goto_set(ISet *s, char X){
    ISet r; r.n=0; int i;
    for(i=0;i<s->n;i++){
        Prod *p=&P[s->it[i].p]; int dot=s->it[i].dot;
        if(p->rhs[0]=='#'||dot>=p->len) continue;
        if(p->rhs[dot]==X){ Item it={s->it[i].p,dot+1}; push(&r,it); }
    }
    closure(&r); return r;
}

int find_state(ISet *s){
    int i,j;
    for(i=0;i<ns;i++){
        if(states[i].n!=s->n) continue;
        int ok=1; for(j=0;j<s->n;j++) if(!has(&states[i],s->it[j])){ok=0;break;}
        if(ok) return i;
    }
    return -1;
}

void build_automaton(){
    Item start={0,0}; states[0].n=0; push(&states[0],start); closure(&states[0]); ns=1;
    memset(GOTO,-1,sizeof(GOTO));
    int i; char all[32]; int na=0;
    /* collect all symbols */
    int k; for(k=0;k<NN;k++) all[na++]=NT[k];
    for(k=0;k<NT_T;k++) all[na++]=TM[k];
    for(i=0;i<ns;i++){
        for(k=0;k<na;k++){
            char X=all[k]; ISet nxt=goto_set(&states[i],X);
            if(!nxt.n) continue;
            int idx=find_state(&nxt);
            if(idx<0){ states[ns]=nxt; idx=ns++; }
            GOTO[i][(unsigned char)X]=idx;
        }
    }
}

/* SLR(1) Action / Goto Tables */
/* action: 0=error, >0=shift(val), <0=reduce(-val), 9999=accept */
#define ACC 9999
int action[MAXS][NT_T], go_nt[MAXS][NN];
int conflict=0;

void set_act(int s, int t, int v){
    if(action[s][t]&&action[s][t]!=v){ printf("CONFLICT state %d term %c\n",s,TM[t]); conflict=1; }
    else action[s][t]=v;
}

void build_slr(){
    memset(action,0,sizeof(action)); memset(go_nt,-1,sizeof(go_nt));
    int i,j;
    for(i=0;i<ns;i++){
        /* shifts from GOTO */
        for(j=0;j<NT_T;j++){
            int nxt=GOTO[i][(unsigned char)TM[j]];
            if(nxt>=0) set_act(i,j,nxt==0?1:nxt); /* nxt is the state */
        }
        /* reduce / accept from complete items */
        int k;
        for(k=0;k<states[i].n;k++){
            Item it=states[i].it[k]; Prod *p=&P[it.p];
            if(p->rhs[0]!='#'&&it.dot<p->len) continue;
            if(it.p==0){ set_act(i,ti('$'),ACC); }
            else {
                int li=ni(p->lhs);
                for(j=0;j<NT_T;j++) if(FOLLOW[li][(unsigned char)TM[j]]) set_act(i,j,-it.p);
            }
        }
        /* goto for non-terminals */
        for(j=0;j<NN;j++){
            int nxt=GOTO[i][(unsigned char)NT[j]];
            go_nt[i][j]=(nxt>=0)?nxt:-1;
        }
    }
}

void print_sets(){
    int i,c; printf("\nFIRST Sets:\n");
    for(i=1;i<NN;i++){  /* skip S' */
        printf("  FIRST(%c) = { ",NT[i]);
        for(c=0;c<128;c++) if(FIRST[i][c]) printf("%c ",c=='#'?'e':c);
        printf("}\n");
    }
    printf("\nFOLLOW Sets:\n");
    for(i=1;i<NN;i++){
        printf("  FOLLOW(%c) = { ",NT[i]);
        for(c=0;c<128;c++) if(FOLLOW[i][c]) printf("%c ",c);
        printf("}\n");
    }
}

void print_table(){
    int i,j;
    printf("\nSLR(1) Parsing Table:\n");
    printf("St | a    b    c    f    g    h    $    | S    B    C    D    E    F\n");
    printf("---+-------------------------------------+-----------------------------\n");
    for(i=0;i<ns;i++){
        printf("%2d | ",i);
        for(j=0;j<NT_T;j++){
            int a=action[i][j];
            if(a==ACC)       printf("acc  ");
            else if(a>0)     printf("s%-4d",a);
            else if(a<0)     printf("r%-4d",-a);
            else             printf("-    ");
        }
        printf("| ");
        for(j=1;j<NN;j++){  /* skip S' column */
            int g=go_nt[i][j];
            if(g>=0) printf("%-5d",g); else printf("-    ");
        }
        printf("\n");
    }
}

void parse(const char *inp){
    char buf[256]; snprintf(buf,sizeof(buf),"%s$",inp);
    int stk[256],top=0; stk[0]=0; int ip=0;

    printf("\n%-22s %-12s %s\n","Stack","Input","Action");
    printf("%-22s %-12s %s\n","----------------------","------------","------");

    while(1){
        char sbuf[128]=""; int k; char tmp[8];
        for(k=0;k<=top;k++){ sprintf(tmp,"%s%d",k?",":"",stk[k]); strcat(sbuf,tmp); }

        int state=stk[top]; char t=buf[ip]; int t_i=ti(t);
        printf("%-22s %-12s ",sbuf,buf+ip);

        if(t_i<0){ printf("ERROR (bad symbol)\n"); printf("=> REJECTED\n"); return; }

        int a=action[state][t_i];
        if(a==0)  { printf("ERROR\n"); printf("=> REJECTED\n"); return; }
        if(a==ACC){ printf("ACCEPT\n"); printf("=> ACCEPTED\n"); return; }
        if(a>0){
            printf("Shift %d\n",a); stk[++top]=a; ip++;
        } else {
            int p=-a; Prod *pr=&P[p];
            printf("Reduce r%d (%c->%s)\n",p,pr->lhs,pr->rhs[0]=='#'?"e":pr->rhs);
            top-=pr->len;
            int g=go_nt[stk[top]][ni(pr->lhs)];
            if(g<0){ printf("=> REJECTED (goto error)\n"); return; }
            stk[++top]=g;
        }
    }
}

int main(){
    char input[256];

    printf("Grammar:\n");
    printf("  S -> aBDh\n  B -> cC\n  C -> bC | e\n");
    printf("  D -> EF\n  E -> g | e\n  F -> f | e\n");

    prod('\'',"S"); prod('S',"aBDh"); prod('B',"cC");
    prod('C',"bC"); prod('C',"#");
    prod('D',"EF"); prod('E',"g"); prod('E',"#");
    prod('F',"f"); prod('F',"#");

    compute_first(); compute_follow();
    build_automaton(); build_slr();

    print_sets();
    print_table();

    if(conflict) printf("\nConflict(s) found — NOT SLR(1).\n");
    else         printf("\nNo conflicts — Grammar is SLR(1).\n");

    printf("\nEnter input string: ");
    scanf("%255s", input);
    parse(input);
    return 0;
}
