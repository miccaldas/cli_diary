#!/usr/bin/env sh

######################################################################
# @author      : mclds (mclds@protonmail.com)
# @file        : mime
# @created     : Wednesday Jul 19, 2023 00:57:31 WEST
#
# @description : 
######################################################################


function mime_type()
{
  file --mime-type -b $*
}

mime_type $*
