extern void csgi__(char *ret_val, ftnlen ret_val_len, integer *ic);
extern void usgi__(char *ret_val, ftnlen ret_val_len, integer *ic);
extern int iand__(integer *, integer *);
extern int ior__(integer *, integer *);
extern int usaxlb__(char *, real *, integer *, real *, char *, integer *, integer *, ftnlen cside_len, ftnlen  ch_len);
extern int uxaxlb__(char *, real *, integer *, real *,  char *, integer *, integer *, ftnlen cside_len, ftnlen ch_len);
extern int uyaxlb__(char *, real *, integer *, real *,  char *, integer *, integer *, ftnlen cside_len, ftnlen ch_len);
extern int usplbl__(char *, integer *, real *, char *, integer *, integer *, ftnlen cside_len, ftnlen ch_len);
extern int uxplbl__(char *, integer *, real *, char *,  integer *, integer *, ftnlen cside_len, ftnlen ch_len);
extern int uyplbl__(char *, integer *, real *, char *,  integer *, integer *, ftnlen cside_len, ftnlen ch_len);
extern int uxplba__(real *, char *, integer *, integer *,  real *, real *, real *, integer *, integer *,  integer *, ftnlen ch_len);
extern int uyplba__(real *, char *, integer *, integer *,  real *, real *, real *, integer *, integer *,  integer *, ftnlen ch_len);
extern int uxplbb__(real *, char *, integer *, integer *,  real *, real *, real *, integer *, integer *,  integer *, real *, logical *, logical *, ftnlen  ch_len);
extern int uyplbb__(real *, char *, integer *, integer *,  real *, real *, real *, integer *, integer *,  integer *, real *, logical *, logical *, ftnlen  ch_len);

#ifndef F2C_INCLUDE
#define F2C_INCLUDE

#define TRUE_ (1)
#define FALSE_ (0)

/* Extern is for use with -E */
#ifndef Extern
#define Extern extern
#endif
/*external read, write*/
typedef struct
{	flag cierr;
	ftnint ciunit;
	flag ciend;
	char *cifmt;
	ftnint cirec;
} cilist;

/*internal read, write*/
typedef struct
{	flag icierr;
	char *iciunit;
	flag iciend;
	char *icifmt;
	ftnint icirlen;
	ftnint icirnum;
} icilist;

/*open*/
typedef struct
{	flag oerr;
	ftnint ounit;
	char *ofnm;
	ftnlen ofnmlen;
	char *osta;
	char *oacc;
	char *ofm;
	ftnint orl;
	char *oblnk;
} olist;

/*close*/
typedef struct
{	flag cerr;
	ftnint cunit;
	char *csta;
} cllist;

/*rewind, backspace, endfile*/
typedef struct
{	flag aerr;
	ftnint aunit;
} alist;

/* inquire */
typedef struct
{	flag inerr;
	ftnint inunit;
	char *infile;
	ftnlen infilen;
	ftnint	*inex;	/*parameters in standard's order*/
	ftnint	*inopen;
	ftnint	*innum;
	ftnint	*innamed;
	char	*inname;
	ftnlen	innamlen;
	char	*inacc;
	ftnlen	inacclen;
	char	*inseq;
	ftnlen	inseqlen;
	char 	*indir;
	ftnlen	indirlen;
	char	*infmt;
	ftnlen	infmtlen;
	char	*inform;
	ftnint	informlen;
	char	*inunf;
	ftnlen	inunflen;
	ftnint	*inrecl;
	ftnint	*innrec;
	char	*inblank;
	ftnlen	inblanklen;
} inlist;

union Multitype {	/* for multiple entry points */
	integer1 g;
	shortint h;
	integer i;
	/* longint j; */
	real r;
	doublereal d;
	complex c;
	doublecomplex z;
	};

typedef union Multitype Multitype;

/*typedef long int Long;*/	/* No longer used; formerly in Namelist */

struct Vardesc {	/* for Namelist */
	char *name;
	char *addr;
	ftnlen *dims;
	int  type;
	};
typedef struct Vardesc Vardesc;

struct Namelist {
	char *name;
	Vardesc **vars;
	int nvars;
	};
typedef struct Namelist Namelist;

#define abs(x) ((x) >= 0 ? (x) : -(x))
#define dabs(x) (doublereal)abs(x)
#define min(a,b) ((a) <= (b) ? (a) : (b))
#define max(a,b) ((a) >= (b) ? (a) : (b))
#define dmin(a,b) (doublereal)min(a,b)
#define dmax(a,b) (doublereal)max(a,b)
#define bit_test(a,b)	((a) >> (b) & 1)
#define bit_clear(a,b)	((a) & ~((uinteger)1 << (b)))
#define bit_set(a,b)	((a) |  ((uinteger)1 << (b)))

/* procedure parameter types for -A and -C++ */

#define F2C_proc_par_types 1
typedef int /* Unknown procedure type */ (*U_fp)();
typedef shortint (*J_fp)();
typedef integer (*I_fp)();
typedef real (*R_fp)();
typedef doublereal (*D_fp)(), (*E_fp)();
typedef /* Complex */ VOID (*C_fp)();
typedef /* Double Complex */ VOID (*Z_fp)();
typedef logical (*L_fp)();
typedef shortlogical (*K_fp)();
typedef /* Character */ VOID (*H_fp)();
typedef /* Subroutine */ int (*S_fp)();
/* E_fp is for real functions when -R is not specified */
typedef VOID C_f;	/* complex function */
typedef VOID H_f;	/* character function */
typedef VOID Z_f;	/* double complex function */
typedef doublereal E_f;	/* real function with -R not specified */

#endif
