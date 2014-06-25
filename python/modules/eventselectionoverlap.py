# -*- coding: utf-8 -*-

"""
"""

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import hashlib
import ROOT

import Artus.HarryPlotter.analysisbase as analysisbase


class EventSelectionOverlap(analysisbase.AnalysisBase):
	def __init__(self):
		super(EventSelectionOverlap, self).__init__()
	
	def run(self, plotData=None):
		super(EventSelectionOverlap, self).run(plotData)
		
		plotData.plotdict["root_histos"] = {}
		for index1, (nick1, tree1) in enumerate(plotData.plotdict.get("root_trees", {}).items()):
			for index2, (nick2, tree2) in enumerate(plotData.plotdict.get("root_trees", {}).items()):
				if index1 != index2 and len(plotData.plotdict["root_histos"]) == 0:
					events1 = EventSelectionOverlap.get_events_set_from_tree(tree1, plotData.plotdict["x_expressions"][index1])
					events2 = EventSelectionOverlap.get_events_set_from_tree(tree2, plotData.plotdict["x_expressions"][index2])
					
					n_events_only1 = len(events1.difference(events2))
					n_events_intersection = len(events1.intersection(events2))
					n_events_only2 = len(events2.difference(events1))
					
					histogram = ROOT.TH1F("histogram_{0}".format(hashlib.md5("_".join([str(n_events_only1),
					                                                                   str(n_events_intersection),
					                                                                   str(n_events_only2)]))),
					                      "Event Selection Overlap", 3, -1.0, 1.0)
					
					histogram.SetBinContent(1, n_events_only1)
					histogram.SetBinContent(2, n_events_intersection)
					histogram.SetBinContent(3, n_events_only2)
					
					plotData.plotdict["root_histos"][nick1 + "_vs_" + nick2] = histogram
	
	@staticmethod
	def get_events_set_from_tree(tree, events_branch_name):
		events = []
		for entry in xrange(tree.GetEntries()):
			tree.GetEntry(entry)
			events.append(getattr(tree, events_branch_name))
		return set(events)
					
