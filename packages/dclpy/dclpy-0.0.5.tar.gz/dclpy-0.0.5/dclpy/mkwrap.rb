#!/usr/bin/ruby
# coding: utf-8
# Usage
# ruby mkwrap.rb cdcl.h > test.txt
# ruby mkwrap.rb cdcln.h >> test.txt
begin
ARGV.each_with_index do |arg, i|
  FNAME=ARGV[0]
end
VALS=['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
CHAR_VALS=[]
CHAR_LEN=[]
modfuncname=""
modfuncname << "static PyMethodDef dclpyMethods[] = {"

includes = <<"INCLUDES"
#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include "dclpy.h"
#include <cdcl.h>
#include <stdbool.h>
INCLUDES

footers = <<"FOOTERS"
static PyModuleDef dclpyModule = {
    PyModuleDef_HEAD_INIT,
    "dclpy",
    NULL,
    -1,
    dclpyMethods
};

PyMODINIT_FUNC
PyInit_dclpy(void) {
    return PyModule_Create(&dclpyModule);
}
FOOTERS


puts includes

#dcl.h ‚Æ‚©‚ð“Ç‚Ýž‚Þ
File.open(FNAME) do |file|
#1s“Ç‚Ýž‚Þ‚Â‚Ü‚èŠÖ”‚Ìî•ñ‚Ì‚Í‚¸
  file.each_line do |labmen|
    CHAR_VALS.clear
    CHAR_LEN.clear
    words=labmen.split
    if words[0] == "extern" then
      fcname=words[2..-1].join(" ").slice!(0..-2).split("(")
      fcname[0].slice!(-1,1)
      if fcname[1] != nil then
        ars=fcname[1].slice!(0..-2).split(",")
        arss=VALS[0..ars.count-1].join(",")
      else
        arss=""
      end

      print("static PyObject *\n")
      print(fcname[0].downcase)
      print("Wrapper(PyObject *self, PyObject *args) {\n")

      if words[1].strip=="void" then
      elsif words[1].strip=="int" then
        print("    int ret;\n")
      elsif words[1].strip=="real" then
        print("    float ret;\n")
      elsif words[1].strip=="logical" then
        print("    int ret;\n")
      end

      arsss=""
      aridx=0
      chidx=0
      ars.each do |labars|
        if labars.strip=="integer *"
          arsss << "i"
          print("    int "+VALS[aridx]+";\n")
          aridx=aridx+1
        elsif labars.strip=="complex *"
          arsss << "D"
          print("    Py_complex "+VALS[aridx]+";\n")
          aridx=aridx+1
        elsif labars.strip=="real *"
          arsss << "f"
          print("    float "+VALS[aridx]+";\n")
          aridx=aridx+1
        elsif labars.strip=="logical *"
          arsss << "p"
          print("    bool "+VALS[aridx]+";\n")
          aridx=aridx+1
        elsif labars.strip.split[0]=="ftnlen"
          chidx=chidx+1
        elsif labars.strip=="char *"
#constant char
          arsss << "s"
          print("    char "+VALS[aridx]+";\n")
          aridx=aridx+1
        end
        
##########logical *
#, ftnlen ch_len
# ftnlen chars_len, ftnlen charz_len
###### char *
####### void
      end
    print("if (!PyArg_ParseTuple(args, \""+arsss+"\"")
    for i in 0..aridx-1 do
      print( ", &" + VALS[i] )
    end
    print(")) {\n")
    print("        return NULL;\n")
    print("}\n")

    if words[1].strip=="void" then
    elsif words[1].strip=="int" then
      print("    ret=")
    end
    if fcname[0].downcase == "usgi_" then
      print("usgi__(&A,0,&B);\n")
    elsif fcname[0].downcase == "csgi_" then
      print("csgi__(&A,0,&B);\n")
    else
      print(fcname[0].downcase+"_(")
    for i in 0..aridx-1 do
      if i != 0 then
        print(",")
      end
      print( " &" + VALS[i] )
    end
    if chidx != 0 then
      for i in 1..chidx do
        print( " ,0" )
      end
    end
    print(");\n")
    end
    
    if words[1].strip!="void" then

      print("return Py_BuildValue(\"")

      if words[1].strip=="int" then
        print("i")
        print("\", ret);\n")
        print("}\n")
      elsif words[1].strip=="real" then
        print("f")
        print("\", ret);\n")
        print("}\n")
      elsif words[1].strip=="logical" then
        print("i")
        print("\", ret);\n")
        print("}\n")
      end
    else
      print("return;")
        print("}\n")
    end



    modfuncname << "{\""
    modfuncname << fcname[0].downcase.delete("_")
    modfuncname << "\","
    modfuncname << fcname[0].downcase
    modfuncname << "Wrapper, METH_VARARGS, NULL},\n"

    end
  end

print(modfuncname)
print("{NULL, NULL, 0, NULL}\n")
print("};\n\n")

puts footers
end















end