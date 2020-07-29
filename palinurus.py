#!/usr/bin/python
import argparse
import os.path
import os
import yaml
import sys
from string import Template
from camelCase import camelCase
""" This is an attempt to make a script to conver kubernetes resources to helm charts
using an externally supplied template to each resource type ( deployment, service ,statefulset )
It is not finished. But currently it can be used for small deployments.
It is work in progress.
"""

class ChartFile(object):
    """  
    This class is to be used as base class for future kubernetes resources types ( deployments, statefulsets, services )
    """
    def __init__(self,name, content, destination = None ):
        with open(name) as fileTemplate:
            chartDef = fileTemplate.read()
            templ = Template(chartDef)
            self.fileContent =  templ.substitute(content)
        if destination is None:
            with open(name, "w+") as chartFile:
                chartFile.write(self.fileContent)
        else:
            with open(destination, "w+") as chartFile:
                chartFile.write(self.fileContent)
            
class Chart(object):
    """
    This class will create a new chart from kubernetes resources"
    """
    def __init__(self,sourceDir):
        yamlList = list()
        for fileName in os.listdir(sourceDir):
            fileName = sourceDir+"/"+fileName
            with open(fileName) as fd:
                textData = fd.read()            
                yamlObject = yaml.load(textData)
                yamlList.append(yamlObject)

        for yobj in yamlList:
            if yobj["kind"] == "Deployment":
                self.name = yobj["metadata"]["name"]
                self.ccname = camelCase(yobj["metadata"]["name"])
                break
        
        print "Creating chart %s"%self.name
        try:
            os.stat(self.name)
        except:
            os.mkdir(self.name)
        try:
            os.stat(self.name+"/templates")
        except:
            os.mkdir(self.name+"/templates")
        # Create Chart.yaml
        contentDict = dict()
        contentDict["name"] = self.name
        contentDict["ccname"] = self.ccname
        chartf = ChartFile("templates/Chart.yaml.template", contentDict, self.name + "/" + "Chart.yaml")
        

        contentDict["cpu"]  = "100m"
        contentDict["memory"]  = "256Mi"
        contentDict["repo"]  = "charts"
        for yobj in yamlList:
            if yobj["kind"] == "Service":
                if "type" in yobj["spec"]:
                    contentDict["serviceType"] = yobj["spec"]["type"]
                else:
                    contentDict["serviceType"] = "ClusterIP"
                contentDict["servicePort"] = yobj["spec"]["ports"][0]["port"]
                contentDict["containerPort"] = yobj["spec"]["ports"][0]["targetPort"]
            if yobj["kind"] == "Deployment":
                if "resources" in  yobj["spec"]["template"]["spec"]["containers"][0]:
                    contentDict["cpu"] = yobj["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["cpu"]
                    contentDict["memory"] = yobj["spec"]["template"]["spec"]["containers"][0]["resources"]["limits"]["memory"]

        if "serviceType" not in contentDict.keys():
            contentDict["serviceType"]="None"
        if "servicePort" not in contentDict.keys():
            contentDict["servicePort"]="None"

        if "containerPort" not in contentDict.keys():
            contentDict["containerPort"]="None"

        # Create the values file
        valuesf = ChartFile("templates/values.yaml", contentDict, self.name + "/values.yaml")
        # Create the helpers file
        valuesf = ChartFile("templates/_helpers.tpl", contentDict, self.name + "/templates/_helpers.tpl")        
        # Create the templates
        for yobj in yamlList:
            contentDict["name"] = self.name
            if yobj["kind"] == "Deployment":
                contentDict["name"] = self.name
                chartf = ChartFile("templates/deployment.yaml.template", contentDict, self.name + "/templates/" + yobj["metadata"]["name"] + "-deployment.yaml")
            if yobj["kind"] == "Service":
                contentDict["name"] = self.name
                chartf = ChartFile("templates/service.yaml.template", contentDict, self.name + "/templates/" + yobj["metadata"]["name"] + "-service.yaml")
            
            
if __name__=="__main__":
    print "This will convert kubernetes resources to a helm chart"
    parser = argparse.ArgumentParser(description='Convert kubernetes resource as helm chart')
    parser.add_argument('--source', help='Kubernetes resource dir',action="store")
    args = parser.parse_args()

    sourceDir = args.source

    if not os.path.isdir(sourceDir):
        print "Directory %s does not exit"%sourceDir
        sys.exit(1)
    else:
        print "Using %s"%sourceDir
        newchart = Chart(sourceDir)
            

