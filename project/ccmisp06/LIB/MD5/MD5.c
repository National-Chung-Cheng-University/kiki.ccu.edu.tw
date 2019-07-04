/*
 * This file was generated automatically by xsubpp version 1.9507 from the 
 * contents of MD5.xs. Do not edit this file, edit MD5.xs instead.
 *
 *	ANY CHANGES MADE HERE WILL BE LOST! 
 *
 */

#line 1 "MD5.xs"
/*
**	Perl Extension for the
**
**	RSA Data Security Inc. MD5 Message-Digest Algorithm
**
**	This module by Neil Winton (N.Winton@axion.bt.co.uk)
**	SCCS ID @(#)MD5.xs	1.7 96/06/28
**
**	This extension may be distributed under the same terms
**	as Perl. The MD5 code is covered by separate copyright and
**	licence, but this does not prohibit distribution under the
**	GNU or Artistic licences. See the file md5c.c or MD5.pm
**	for more details.
*/

#ifdef __cplusplus
extern "C" {
#endif
#include "EXTERN.h"
#include "perl.h"
#include "XSUB.h"

#include "global.h"
#include "md5.h"

/*
** The following macro re-definitions added to work around a problem on
** Solaris where the original MD5 routines are already in /lib/libnsl.a.
** This causes dynamic linking of the module to fail.
** Thanks to Ken Pizzini (ken@spry.com) for finally nailing this one!
*/

#define MD5Init		MD5Init_perl
#define MD5Update	MD5Update_perl
#define MD5Final	MD5Final_perl

typedef MD5_CTX	*MD5;

#ifdef __cplusplus
}
#endif


#line 54 "MD5.c"
XS(XS_MD5_new)
{
    dXSARGS;
    if (items < 0 || items > 1)
	croak("Usage: MD5::new(packname = \"MD5\")");
    {
	char *	packname;
	MD5	RETVAL;

	if (items < 1)
	    packname = "MD5";
	else {
	    packname = (char *)SvPV(ST(0),PL_na);
	}
#line 52 "MD5.xs"
	{
	    RETVAL = (MD5_CTX *)safemalloc(sizeof(MD5_CTX));
	    MD5Init(RETVAL);
	}
#line 74 "MD5.c"
	ST(0) = sv_newmortal();
	sv_setref_pv(ST(0), "MD5", (void*)RETVAL);
    }
    XSRETURN(1);
}

XS(XS_MD5_DESTROY)
{
    dXSARGS;
    if (items != 1)
	croak("Usage: MD5::DESTROY(context)");
    {
	MD5	context;

	if (SvROK(ST(0))) {
	    IV tmp = SvIV((SV*)SvRV(ST(0)));
	    context = (MD5) tmp;
	}
	else
	    croak("context is not a reference");
#line 63 "MD5.xs"
	{
	    safefree((char *)context);
	}
#line 99 "MD5.c"
    }
    XSRETURN_EMPTY;
}

XS(XS_MD5_reset)
{
    dXSARGS;
    if (items != 1)
	croak("Usage: MD5::reset(context)");
    {
	MD5	context;

	if (sv_derived_from(ST(0), "MD5")) {
	    IV tmp = SvIV((SV*)SvRV(ST(0)));
	    context = (MD5) tmp;
	}
	else
	    croak("context is not of type MD5");
#line 71 "MD5.xs"
	{
	    MD5Init(context);
	}
#line 122 "MD5.c"
    }
    XSRETURN_EMPTY;
}

XS(XS_MD5_add)
{
    dXSARGS;
    if (items < 1)
	croak("Usage: MD5::add(context, ...)");
    {
	MD5	context;

	if (sv_derived_from(ST(0), "MD5")) {
	    IV tmp = SvIV((SV*)SvRV(ST(0)));
	    context = (MD5) tmp;
	}
	else
	    croak("context is not of type MD5");
#line 79 "MD5.xs"
	{
	    SV *svdata;
	    STRLEN len;
	    unsigned char *data;
	    int i;

	    for (i = 1; i < items; i++)
	    {
		data = (unsigned char *)(SvPV(ST(i), len));
		MD5Update(context, data, len);
	    }
	}
#line 154 "MD5.c"
    }
    XSRETURN_EMPTY;
}

XS(XS_MD5_digest)
{
    dXSARGS;
    if (items != 1)
	croak("Usage: MD5::digest(context)");
    {
	MD5	context;
	SV *	RETVAL;

	if (sv_derived_from(ST(0), "MD5")) {
	    IV tmp = SvIV((SV*)SvRV(ST(0)));
	    context = (MD5) tmp;
	}
	else
	    croak("context is not of type MD5");
#line 96 "MD5.xs"
	{
	    unsigned char digeststr[16];

	    MD5Final(digeststr, context);
	    ST(0) = sv_2mortal(newSVpv((char *)digeststr, 16));
	}
#line 181 "MD5.c"
    }
    XSRETURN(1);
}

#ifdef __cplusplus
extern "C"
#endif
XS(boot_MD5)
{
    dXSARGS;
    char* file = __FILE__;

    XS_VERSION_BOOTCHECK ;

        newXS("MD5::new", XS_MD5_new, file);
        newXS("MD5::DESTROY", XS_MD5_DESTROY, file);
        newXS("MD5::reset", XS_MD5_reset, file);
        newXS("MD5::add", XS_MD5_add, file);
        newXS("MD5::digest", XS_MD5_digest, file);
    XSRETURN_YES;
}

