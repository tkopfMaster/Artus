# -*- coding: utf-8 -*-

import logging
import Artus.Utility.logger as logger
log = logging.getLogger(__name__)

import Artus.HarryPlotter.analysisbase as analysisbase
import Artus.HarryPlotter.utility.roottools as roottools


class AddHistograms(analysisbase.AnalysisBase):
	"""Create sum of histograms. This module does exactly the same as SumOfHistograms, but is can enable different addition steps together with this module."""

	def modify_argument_parser(self, parser, args):
		super(AddHistograms, self).modify_argument_parser(parser, args)

		self.add_histograms_options = parser.add_argument_group("{} options".format(self.name()))
		self.add_histograms_options.add_argument(
				"--add-nicks", nargs="+",
				help="Nick names (whitespace separated) for the histograms to be added"
		)
		self.add_histograms_options.add_argument(
				"--add-scale-factors", nargs="+",
				help="Scale factor (whitespace separated) for the histograms to be added [Default: 1]."
		)
		self.add_histograms_options.add_argument(
				"--add-result-nicks", nargs="+",
				help="Nick names for the resulting sum histograms."
		)
		self.add_histograms_options.add_argument(
				"--add-result-position",
				help="Position where added histogram is inserted in draw order. 0=first, 1=second etc. (Default: after last nick that was used to add)", default=None
		)
	def prepare_args(self, parser, plotData):
		super(AddHistograms, self).prepare_args(parser, plotData)
		self.prepare_list_args(plotData, ["add_nicks", "add_result_nicks", "add_scale_factors", "add_result_position"])
		
		for index, (add_nicks, add_result_nick, add_scale_factors) in enumerate(zip(
				*[plotData.plotdict[k] for k in ["add_nicks", "add_result_nicks", "add_scale_factors"]]
		)):
			plotData.plotdict["add_nicks"][index] = add_nicks.split()
			if add_scale_factors is None:
				plotData.plotdict["add_scale_factors"][index] = [1] * len(add_nicks.split())
			else:
				plotData.plotdict["add_scale_factors"][index] = [float(add_scale_factor) for add_scale_factor in add_scale_factors.split()]
			if add_result_nick is None:
				plotData.plotdict["add_result_nicks"][index] = "add_{}".format(
						"_".join(plotData.plotdict["add_nicks"][index]),
				)
			if not plotData.plotdict["add_result_nicks"][index] in plotData.plotdict["nicks"]:
				if not plotData.plotdict["add_result_position"][0]:
					plotData.plotdict["nicks"].insert(
							plotData.plotdict["nicks"].index(plotData.plotdict["add_nicks"][index][-1])+1,
							plotData.plotdict["add_result_nicks"][index]
					)
				else:
					plotData.plotdict["nicks"].insert(
							plotData.plotdict["add_result_position"][0],
							plotData.plotdict["add_result_nicks"][index]
					)

	def run(self, plotData=None):
		super(AddHistograms, self).run(plotData)
		
		for add_nicks, add_scale_factors, add_result_nick in zip(
				*[plotData.plotdict[k] for k in ["add_nicks", "add_scale_factors", "add_result_nicks"]]
		):
			
			log.debug("AddHistograms: "+add_result_nick+" = "+(" + ".join([str(scale)+"*"+nick for nick, scale in zip(add_nicks, add_scale_factors)])))
			plotData.plotdict["root_objects"][add_result_nick] = roottools.RootTools.add_root_histograms(
					*[plotData.plotdict["root_objects"][nick] for nick in add_nicks],
					scale_factors=add_scale_factors
			)

