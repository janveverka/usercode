# minimalistic config file to copy / merge cmssw datasets
# veverka@caltech.edu, 2008-12-16

import FWCore.ParameterSet.Config as cms

process = cms.Process('MERGE')

process.load("FWCore.MessageLogger.MessageLogger_cfi")
process.MessageLogger.cerr.FwkReport.reportEvery = 1000

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
   )
)
sourcePath = "/uscms/home/veverka/work/jpsi/CMSSW_3_7_0_patch3/src/JPsi/MuMu/test/crab/crab_0_100701_151308/res/"
fileList = """
DimuonSkim_100_1_RyP.root  DimuonSkim_254_1_raQ.root  DimuonSkim_407_1_CVi.root  DimuonSkim_560_1_xe7.root
DimuonSkim_101_1_osM.root  DimuonSkim_255_1_wHy.root  DimuonSkim_408_1_bWm.root  DimuonSkim_561_1_sBs.root
DimuonSkim_102_1_lt1.root  DimuonSkim_256_1_QHC.root  DimuonSkim_409_1_o5P.root  DimuonSkim_562_1_2P7.root
DimuonSkim_103_1_SeL.root  DimuonSkim_257_1_16f.root  DimuonSkim_40_1_hFE.root   DimuonSkim_563_1_0yf.root
DimuonSkim_104_1_KLi.root  DimuonSkim_258_1_KZ6.root  DimuonSkim_410_1_AUa.root  DimuonSkim_564_1_yp3.root
DimuonSkim_105_1_DrM.root  DimuonSkim_259_1_4eK.root  DimuonSkim_411_1_nlJ.root  DimuonSkim_565_1_6fY.root
DimuonSkim_106_1_nLI.root  DimuonSkim_25_1_mIp.root   DimuonSkim_412_1_HCJ.root  DimuonSkim_566_1_vOs.root
DimuonSkim_107_1_WQW.root  DimuonSkim_260_1_9Jb.root  DimuonSkim_413_1_P4q.root  DimuonSkim_567_1_XV7.root
DimuonSkim_108_1_Cn7.root  DimuonSkim_261_1_4aH.root  DimuonSkim_414_1_wjB.root  DimuonSkim_568_1_iIB.root
DimuonSkim_109_1_PWn.root  DimuonSkim_262_1_Fmy.root  DimuonSkim_415_1_YR4.root  DimuonSkim_569_1_Qcq.root
DimuonSkim_10_1_Ty1.root   DimuonSkim_263_1_0lI.root  DimuonSkim_416_1_JyL.root  DimuonSkim_56_1_CgC.root
DimuonSkim_110_1_NLw.root  DimuonSkim_264_1_R5l.root  DimuonSkim_417_1_tSG.root  DimuonSkim_570_1_RAc.root
DimuonSkim_111_1_1NG.root  DimuonSkim_265_1_jff.root  DimuonSkim_418_1_Vkd.root  DimuonSkim_571_1_pMs.root
DimuonSkim_112_1_Ik1.root  DimuonSkim_266_1_ukf.root  DimuonSkim_419_1_UUK.root  DimuonSkim_572_1_q0h.root
DimuonSkim_113_1_Jqe.root  DimuonSkim_267_1_zXO.root  DimuonSkim_41_1_6Np.root   DimuonSkim_573_1_typ.root
DimuonSkim_114_1_O0z.root  DimuonSkim_268_1_d9C.root  DimuonSkim_420_1_89h.root  DimuonSkim_574_1_L6D.root
DimuonSkim_115_1_53a.root  DimuonSkim_269_1_pQV.root  DimuonSkim_421_1_jzO.root  DimuonSkim_575_1_qJG.root
DimuonSkim_116_1_vhi.root  DimuonSkim_26_1_PPw.root   DimuonSkim_422_1_29M.root  DimuonSkim_576_1_QW2.root
DimuonSkim_117_1_TsQ.root  DimuonSkim_270_1_uKK.root  DimuonSkim_423_1_ZgB.root  DimuonSkim_577_1_847.root
DimuonSkim_118_1_RCV.root  DimuonSkim_271_1_88Q.root  DimuonSkim_424_1_5zA.root  DimuonSkim_578_1_AbT.root
DimuonSkim_119_1_Bj2.root  DimuonSkim_272_1_kmZ.root  DimuonSkim_425_1_L13.root  DimuonSkim_579_1_tWl.root
DimuonSkim_11_1_iAZ.root   DimuonSkim_273_1_hWj.root  DimuonSkim_426_1_Lbl.root  DimuonSkim_57_1_619.root
DimuonSkim_120_1_OhF.root  DimuonSkim_274_1_GDs.root  DimuonSkim_427_1_hNs.root  DimuonSkim_580_1_lJs.root
DimuonSkim_121_1_bYn.root  DimuonSkim_275_1_ruU.root  DimuonSkim_428_1_8zC.root  DimuonSkim_581_1_h8i.root
DimuonSkim_122_1_b27.root  DimuonSkim_276_1_nG4.root  DimuonSkim_429_1_hGP.root  DimuonSkim_582_1_MUM.root
DimuonSkim_123_1_dNr.root  DimuonSkim_277_1_rm3.root  DimuonSkim_42_1_SiE.root   DimuonSkim_583_1_n5p.root
DimuonSkim_124_1_JSB.root  DimuonSkim_278_1_E6Z.root  DimuonSkim_430_1_40A.root  DimuonSkim_584_1_yGd.root
DimuonSkim_125_1_k5t.root  DimuonSkim_279_1_zcs.root  DimuonSkim_431_1_Qg2.root  DimuonSkim_585_1_r3M.root
DimuonSkim_126_1_y3s.root  DimuonSkim_27_1_vgr.root   DimuonSkim_432_1_iVY.root  DimuonSkim_586_1_IbN.root
DimuonSkim_127_1_qjy.root  DimuonSkim_280_1_LIt.root  DimuonSkim_433_1_sqT.root  DimuonSkim_587_1_PjO.root
DimuonSkim_128_1_Y7a.root  DimuonSkim_281_1_CF0.root  DimuonSkim_434_1_USR.root  DimuonSkim_588_1_S7D.root
DimuonSkim_129_1_HZ3.root  DimuonSkim_282_1_fZ2.root  DimuonSkim_435_1_pTJ.root  DimuonSkim_589_1_46y.root
DimuonSkim_12_1_N6U.root   DimuonSkim_283_1_XWp.root  DimuonSkim_436_1_nzJ.root  DimuonSkim_58_1_Cfd.root
DimuonSkim_130_1_JCF.root  DimuonSkim_284_1_YZp.root  DimuonSkim_437_1_WEv.root  DimuonSkim_590_1_Vi7.root
DimuonSkim_131_1_yHb.root  DimuonSkim_285_1_ftJ.root  DimuonSkim_438_1_CZm.root  DimuonSkim_591_1_xfn.root
DimuonSkim_132_1_9Sv.root  DimuonSkim_286_1_r9b.root  DimuonSkim_439_1_TB0.root  DimuonSkim_592_1_iFA.root
DimuonSkim_133_1_YDK.root  DimuonSkim_287_1_CPv.root  DimuonSkim_43_1_QH5.root   DimuonSkim_593_1_aEC.root
DimuonSkim_134_1_o0L.root  DimuonSkim_288_1_anw.root  DimuonSkim_440_1_OI8.root  DimuonSkim_594_1_kgD.root
DimuonSkim_135_1_9AL.root  DimuonSkim_289_1_yCr.root  DimuonSkim_441_1_jQm.root  DimuonSkim_595_1_xBn.root
DimuonSkim_136_1_OIf.root  DimuonSkim_28_1_Nhu.root   DimuonSkim_442_1_40E.root  DimuonSkim_596_1_xVy.root
DimuonSkim_137_1_r2B.root  DimuonSkim_290_1_Xqg.root  DimuonSkim_443_1_8Mf.root  DimuonSkim_597_1_JKD.root
DimuonSkim_138_1_lop.root  DimuonSkim_291_1_YH4.root  DimuonSkim_444_1_Hgq.root  DimuonSkim_598_1_SzI.root
DimuonSkim_139_1_nB2.root  DimuonSkim_292_1_Xt3.root  DimuonSkim_445_1_XpC.root  DimuonSkim_599_1_dOS.root
DimuonSkim_13_1_Ii9.root   DimuonSkim_293_1_icr.root  DimuonSkim_446_1_YKZ.root  DimuonSkim_59_1_GeB.root
DimuonSkim_140_1_pSO.root  DimuonSkim_294_1_V4M.root  DimuonSkim_447_1_v8G.root  DimuonSkim_5_1_z5l.root
DimuonSkim_141_1_jGq.root  DimuonSkim_295_1_n5I.root  DimuonSkim_448_1_1Lu.root  DimuonSkim_600_1_F7B.root
DimuonSkim_142_1_w0X.root  DimuonSkim_296_1_ILr.root  DimuonSkim_449_1_wMF.root  DimuonSkim_601_1_4p6.root
DimuonSkim_143_1_zYF.root  DimuonSkim_297_1_poU.root  DimuonSkim_44_1_T06.root   DimuonSkim_602_1_Re4.root
DimuonSkim_144_1_Bx0.root  DimuonSkim_298_1_HvB.root  DimuonSkim_450_1_AV4.root  DimuonSkim_603_1_Zg2.root
DimuonSkim_145_1_Huv.root  DimuonSkim_299_1_QZJ.root  DimuonSkim_451_1_U3w.root  DimuonSkim_604_1_0H9.root
DimuonSkim_146_1_dXe.root  DimuonSkim_29_1_Nd8.root   DimuonSkim_452_1_g02.root  DimuonSkim_605_1_YOM.root
DimuonSkim_147_1_Zcj.root  DimuonSkim_2_1_iJ0.root    DimuonSkim_453_1_vaa.root  DimuonSkim_606_1_wLF.root
DimuonSkim_148_1_sJT.root  DimuonSkim_300_1_Wmi.root  DimuonSkim_454_1_T4v.root  DimuonSkim_607_1_ICr.root
DimuonSkim_149_1_7NL.root  DimuonSkim_301_1_l3B.root  DimuonSkim_455_1_Vld.root  DimuonSkim_608_1_0nL.root
DimuonSkim_14_1_9Od.root   DimuonSkim_302_1_0nA.root  DimuonSkim_456_1_Ugv.root  DimuonSkim_609_1_5Hg.root
DimuonSkim_150_1_4Sc.root  DimuonSkim_303_1_zsj.root  DimuonSkim_457_1_D8P.root  DimuonSkim_60_1_buH.root
DimuonSkim_151_1_RqF.root  DimuonSkim_304_1_Tz5.root  DimuonSkim_458_1_ELS.root  DimuonSkim_610_1_KDA.root
DimuonSkim_152_1_R4m.root  DimuonSkim_305_1_3Fd.root  DimuonSkim_459_1_Esm.root  DimuonSkim_611_1_kDZ.root
DimuonSkim_153_1_TNn.root  DimuonSkim_306_1_aZm.root  DimuonSkim_45_1_e7h.root   DimuonSkim_612_1_8fQ.root
DimuonSkim_154_1_HmH.root  DimuonSkim_307_1_l3e.root  DimuonSkim_460_1_HIJ.root  DimuonSkim_613_1_jr8.root
DimuonSkim_155_1_o2u.root  DimuonSkim_308_1_JB7.root  DimuonSkim_461_1_nqI.root  DimuonSkim_614_1_uMC.root
DimuonSkim_156_1_QVa.root  DimuonSkim_309_1_05D.root  DimuonSkim_462_1_wC1.root  DimuonSkim_615_1_3cV.root
DimuonSkim_157_1_Wa4.root  DimuonSkim_30_1_T5D.root   DimuonSkim_463_1_FNj.root  DimuonSkim_616_1_Sws.root
DimuonSkim_158_1_Alg.root  DimuonSkim_310_1_GqH.root  DimuonSkim_464_1_Eoc.root  DimuonSkim_617_1_2VU.root
DimuonSkim_159_1_o1X.root  DimuonSkim_311_1_53Y.root  DimuonSkim_465_1_G5q.root  DimuonSkim_618_1_Q8X.root
DimuonSkim_15_1_hND.root   DimuonSkim_312_1_kLq.root  DimuonSkim_466_1_kLr.root  DimuonSkim_619_1_x15.root
DimuonSkim_160_1_owq.root  DimuonSkim_313_1_lNt.root  DimuonSkim_467_1_PnL.root  DimuonSkim_61_1_kLL.root
DimuonSkim_161_1_n3c.root  DimuonSkim_314_1_Dqc.root  DimuonSkim_468_1_5Rv.root  DimuonSkim_620_1_U5t.root
DimuonSkim_162_1_awI.root  DimuonSkim_315_1_jvZ.root  DimuonSkim_469_1_qMx.root  DimuonSkim_621_1_Wjg.root
DimuonSkim_163_1_l66.root  DimuonSkim_316_1_O4M.root  DimuonSkim_46_1_Sva.root   DimuonSkim_622_1_ivg.root
DimuonSkim_164_1_MNY.root  DimuonSkim_317_1_9WP.root  DimuonSkim_470_1_5Nr.root  DimuonSkim_623_1_7nA.root
DimuonSkim_165_1_x0S.root  DimuonSkim_318_1_2vA.root  DimuonSkim_471_1_8Hn.root  DimuonSkim_624_1_SuY.root
DimuonSkim_166_1_oHL.root  DimuonSkim_319_1_fCS.root  DimuonSkim_472_1_1bF.root  DimuonSkim_625_1_Zj2.root
DimuonSkim_167_1_H5t.root  DimuonSkim_31_1_eMp.root   DimuonSkim_473_1_6zk.root  DimuonSkim_626_1_nHp.root
DimuonSkim_168_1_Fe3.root  DimuonSkim_320_1_9Ff.root  DimuonSkim_474_1_Re7.root  DimuonSkim_627_1_hDr.root
DimuonSkim_169_1_keV.root  DimuonSkim_321_1_yd4.root  DimuonSkim_475_1_pzR.root  DimuonSkim_628_1_u1W.root
DimuonSkim_16_1_pz7.root   DimuonSkim_322_1_LwJ.root  DimuonSkim_476_1_TkG.root  DimuonSkim_629_1_2Gs.root
DimuonSkim_170_1_aJQ.root  DimuonSkim_323_1_YOv.root  DimuonSkim_477_1_I97.root  DimuonSkim_62_1_Sc2.root
DimuonSkim_171_1_qM8.root  DimuonSkim_324_1_Ps8.root  DimuonSkim_478_1_biC.root  DimuonSkim_630_1_IrN.root
DimuonSkim_172_1_aOx.root  DimuonSkim_325_1_1ZP.root  DimuonSkim_479_1_H12.root  DimuonSkim_631_1_tTl.root
DimuonSkim_173_1_xPP.root  DimuonSkim_326_1_FdY.root  DimuonSkim_47_1_oRo.root   DimuonSkim_632_1_OAP.root
DimuonSkim_174_1_U4j.root  DimuonSkim_327_1_1e2.root  DimuonSkim_480_1_v9q.root  DimuonSkim_633_1_mZV.root
DimuonSkim_175_1_dkD.root  DimuonSkim_328_1_yYo.root  DimuonSkim_481_1_YnY.root  DimuonSkim_634_1_8NG.root
DimuonSkim_176_1_Gao.root  DimuonSkim_329_1_7rO.root  DimuonSkim_482_1_D4F.root  DimuonSkim_635_1_GWG.root
DimuonSkim_177_1_VHy.root  DimuonSkim_32_1_HB5.root   DimuonSkim_483_1_7KP.root  DimuonSkim_636_1_wGr.root
DimuonSkim_178_1_7KS.root  DimuonSkim_330_1_oU8.root  DimuonSkim_484_1_8of.root  DimuonSkim_637_1_dGX.root
DimuonSkim_179_1_3ea.root  DimuonSkim_331_1_mO5.root  DimuonSkim_485_1_LfL.root  DimuonSkim_638_1_xj6.root
DimuonSkim_17_1_D7q.root   DimuonSkim_332_1_bsN.root  DimuonSkim_486_1_WiX.root  DimuonSkim_639_1_3D3.root
DimuonSkim_180_1_66y.root  DimuonSkim_333_1_T4U.root  DimuonSkim_487_1_oDt.root  DimuonSkim_63_1_mNy.root
DimuonSkim_181_1_Smf.root  DimuonSkim_334_1_p8n.root  DimuonSkim_488_1_x3m.root  DimuonSkim_640_1_2vb.root
DimuonSkim_182_1_NVc.root  DimuonSkim_335_1_fnl.root  DimuonSkim_489_1_917.root  DimuonSkim_641_1_jJz.root
DimuonSkim_183_1_vQ3.root  DimuonSkim_336_1_e7w.root  DimuonSkim_48_1_gh0.root   DimuonSkim_642_1_75D.root
DimuonSkim_184_1_f5j.root  DimuonSkim_337_1_8HF.root  DimuonSkim_490_1_1gI.root  DimuonSkim_643_1_ZvW.root
DimuonSkim_185_1_skp.root  DimuonSkim_338_1_wyX.root  DimuonSkim_491_1_MmX.root  DimuonSkim_644_1_2Hc.root
DimuonSkim_186_1_cUa.root  DimuonSkim_339_1_Map.root  DimuonSkim_492_1_2Od.root  DimuonSkim_645_1_QGM.root
DimuonSkim_187_1_FZh.root  DimuonSkim_33_1_7Ru.root   DimuonSkim_493_1_Ya7.root  DimuonSkim_646_1_t9K.root
DimuonSkim_188_1_wqs.root  DimuonSkim_340_1_ik8.root  DimuonSkim_494_1_SXp.root  DimuonSkim_647_1_Wc2.root
DimuonSkim_189_1_5FR.root  DimuonSkim_341_1_cco.root  DimuonSkim_495_1_jRJ.root  DimuonSkim_648_1_ySe.root
DimuonSkim_18_1_nPg.root   DimuonSkim_342_1_XQA.root  DimuonSkim_496_1_mhn.root  DimuonSkim_649_1_2rB.root
DimuonSkim_190_1_DkT.root  DimuonSkim_343_1_uOc.root  DimuonSkim_497_1_s6z.root  DimuonSkim_64_1_8br.root
DimuonSkim_191_1_Iuy.root  DimuonSkim_344_1_iwO.root  DimuonSkim_498_1_Bby.root  DimuonSkim_650_1_KzK.root
DimuonSkim_192_1_An5.root  DimuonSkim_345_1_I04.root  DimuonSkim_499_1_zi7.root  DimuonSkim_651_1_uxv.root
DimuonSkim_193_1_Mqp.root  DimuonSkim_346_1_R6O.root  DimuonSkim_49_1_91N.root   DimuonSkim_652_1_bqP.root
DimuonSkim_194_1_Xvw.root  DimuonSkim_347_1_wVU.root  DimuonSkim_4_1_zO2.root    DimuonSkim_653_1_MOc.root
DimuonSkim_195_1_k0E.root  DimuonSkim_348_1_p6y.root  DimuonSkim_500_1_wXS.root  DimuonSkim_654_1_mAQ.root
DimuonSkim_196_1_F9W.root  DimuonSkim_349_1_fXG.root  DimuonSkim_501_1_Ydm.root  DimuonSkim_655_1_K43.root
DimuonSkim_197_1_TMd.root  DimuonSkim_34_1_NNV.root   DimuonSkim_502_1_3ha.root  DimuonSkim_656_1_q2o.root
DimuonSkim_198_1_jvs.root  DimuonSkim_350_1_yHR.root  DimuonSkim_503_1_qJz.root  DimuonSkim_657_1_spJ.root
DimuonSkim_199_1_0vq.root  DimuonSkim_351_1_8yq.root  DimuonSkim_504_1_wWE.root  DimuonSkim_658_1_Fu9.root
DimuonSkim_19_1_Yhv.root   DimuonSkim_352_1_2Rc.root  DimuonSkim_505_1_jpr.root  DimuonSkim_659_1_CSJ.root
DimuonSkim_1_1_6f5.root    DimuonSkim_353_1_M1r.root  DimuonSkim_506_1_0Wg.root  DimuonSkim_65_1_5ac.root
DimuonSkim_200_1_8x6.root  DimuonSkim_354_1_QjC.root  DimuonSkim_507_1_jlk.root  DimuonSkim_660_1_GUH.root
DimuonSkim_201_1_Xde.root  DimuonSkim_355_1_tQ2.root  DimuonSkim_508_1_ZpC.root  DimuonSkim_661_1_HTX.root
DimuonSkim_202_1_nJ8.root  DimuonSkim_356_1_HO3.root  DimuonSkim_509_1_bJ6.root  DimuonSkim_662_1_ttv.root
DimuonSkim_203_1_Fhv.root  DimuonSkim_357_1_hnp.root  DimuonSkim_50_1_oxW.root   DimuonSkim_663_1_sKF.root
DimuonSkim_204_1_zLp.root  DimuonSkim_358_1_WjV.root  DimuonSkim_510_1_KFB.root  DimuonSkim_664_1_lJk.root
DimuonSkim_205_1_id7.root  DimuonSkim_359_1_rvC.root  DimuonSkim_511_1_Lyz.root  DimuonSkim_665_1_Jwm.root
DimuonSkim_206_1_Xyb.root  DimuonSkim_35_1_AWI.root   DimuonSkim_512_1_2HH.root  DimuonSkim_666_1_fln.root
DimuonSkim_207_1_AwT.root  DimuonSkim_360_1_CqM.root  DimuonSkim_513_1_U0J.root  DimuonSkim_667_1_EPH.root
DimuonSkim_208_1_JPy.root  DimuonSkim_361_1_Iho.root  DimuonSkim_514_1_yJN.root  DimuonSkim_668_1_8k5.root
DimuonSkim_209_1_ksR.root  DimuonSkim_362_1_4Sm.root  DimuonSkim_515_1_WUS.root  DimuonSkim_669_1_BmO.root
DimuonSkim_20_1_mkj.root   DimuonSkim_363_1_VUG.root  DimuonSkim_516_1_MV7.root  DimuonSkim_66_1_Czm.root
DimuonSkim_210_1_APQ.root  DimuonSkim_364_1_ePS.root  DimuonSkim_517_1_Orp.root  DimuonSkim_670_1_7on.root
DimuonSkim_211_1_EPc.root  DimuonSkim_365_1_eQQ.root  DimuonSkim_518_1_FW3.root  DimuonSkim_671_1_ajX.root
DimuonSkim_212_1_ojE.root  DimuonSkim_366_1_WFT.root  DimuonSkim_519_1_QHb.root  DimuonSkim_672_1_HyB.root
DimuonSkim_213_1_CSE.root  DimuonSkim_367_1_bWk.root  DimuonSkim_51_1_ytb.root   DimuonSkim_673_1_StG.root
DimuonSkim_214_1_7MG.root  DimuonSkim_368_1_1ua.root  DimuonSkim_520_1_NLJ.root  DimuonSkim_674_1_XIB.root
DimuonSkim_215_1_sEj.root  DimuonSkim_369_1_81Q.root  DimuonSkim_521_1_8qt.root  DimuonSkim_675_1_eIx.root
DimuonSkim_216_1_0Ea.root  DimuonSkim_36_1_nQl.root   DimuonSkim_522_1_l7C.root  DimuonSkim_676_1_LRD.root
DimuonSkim_217_1_WU5.root  DimuonSkim_370_1_zJ9.root  DimuonSkim_523_1_oI6.root  DimuonSkim_677_1_Az6.root
DimuonSkim_218_1_vws.root  DimuonSkim_371_1_dpf.root  DimuonSkim_524_1_svV.root  DimuonSkim_678_1_nB3.root
DimuonSkim_219_1_VbN.root  DimuonSkim_372_1_Opp.root  DimuonSkim_525_1_s84.root  DimuonSkim_679_1_kku.root
DimuonSkim_21_1_lec.root   DimuonSkim_373_1_fRd.root  DimuonSkim_526_1_aCH.root  DimuonSkim_67_1_sAs.root
DimuonSkim_220_1_SCG.root  DimuonSkim_374_1_4M0.root  DimuonSkim_527_1_KJ1.root  DimuonSkim_68_1_IjV.root
DimuonSkim_221_1_Dxw.root  DimuonSkim_375_1_Da4.root  DimuonSkim_528_1_MYd.root  DimuonSkim_69_1_MGJ.root
DimuonSkim_222_1_oHo.root  DimuonSkim_376_1_z6v.root  DimuonSkim_529_1_XD2.root  DimuonSkim_6_1_Su8.root
DimuonSkim_223_1_NV2.root  DimuonSkim_377_1_kuc.root  DimuonSkim_52_1_J9U.root   DimuonSkim_70_1_JRq.root
DimuonSkim_224_1_lHK.root  DimuonSkim_378_1_7Yt.root  DimuonSkim_530_1_2Me.root  DimuonSkim_71_1_t5N.root
DimuonSkim_225_1_o6g.root  DimuonSkim_379_1_Pra.root  DimuonSkim_531_1_sLP.root  DimuonSkim_72_1_wyK.root
DimuonSkim_226_1_s2x.root  DimuonSkim_37_1_JyT.root   DimuonSkim_532_1_bCD.root  DimuonSkim_73_1_hEc.root
DimuonSkim_227_1_i4v.root  DimuonSkim_380_1_VZZ.root  DimuonSkim_533_1_MII.root  DimuonSkim_74_1_8gQ.root
DimuonSkim_228_1_5ej.root  DimuonSkim_381_1_iJd.root  DimuonSkim_534_1_HoB.root  DimuonSkim_75_1_aVn.root
DimuonSkim_229_1_KYh.root  DimuonSkim_382_1_Zjh.root  DimuonSkim_535_1_mhr.root  DimuonSkim_76_1_wpR.root
DimuonSkim_22_1_pLX.root   DimuonSkim_383_1_RMo.root  DimuonSkim_536_1_PyN.root  DimuonSkim_77_1_2E1.root
DimuonSkim_230_1_eGT.root  DimuonSkim_384_1_vwr.root  DimuonSkim_537_1_VS3.root  DimuonSkim_78_1_LSJ.root
DimuonSkim_231_1_F3s.root  DimuonSkim_385_1_64M.root  DimuonSkim_538_1_RaG.root  DimuonSkim_79_1_cvu.root
DimuonSkim_232_1_XT5.root  DimuonSkim_386_1_agH.root  DimuonSkim_539_1_TZw.root  DimuonSkim_7_1_GI1.root
DimuonSkim_233_1_e4M.root  DimuonSkim_387_1_bWA.root  DimuonSkim_53_1_UYB.root   DimuonSkim_80_1_YBo.root
DimuonSkim_234_1_CO0.root  DimuonSkim_388_1_FC5.root  DimuonSkim_540_1_cRv.root  DimuonSkim_81_1_haU.root
DimuonSkim_235_1_keD.root  DimuonSkim_389_1_Dya.root  DimuonSkim_541_1_8Kq.root  DimuonSkim_82_1_jqP.root
DimuonSkim_236_1_EZK.root  DimuonSkim_38_1_hso.root   DimuonSkim_542_1_Grt.root  DimuonSkim_83_1_ksc.root
DimuonSkim_237_1_7fu.root  DimuonSkim_390_1_QkU.root  DimuonSkim_543_1_pSU.root  DimuonSkim_84_1_47y.root
DimuonSkim_238_1_WOa.root  DimuonSkim_391_1_LUi.root  DimuonSkim_544_1_dge.root  DimuonSkim_85_1_2nj.root
DimuonSkim_239_1_q7T.root  DimuonSkim_392_1_HBD.root  DimuonSkim_545_1_M4s.root  DimuonSkim_86_1_mRw.root
DimuonSkim_23_1_qYX.root   DimuonSkim_393_1_WXD.root  DimuonSkim_546_1_mNn.root  DimuonSkim_87_1_tY1.root
DimuonSkim_240_1_VbI.root  DimuonSkim_394_1_8SJ.root  DimuonSkim_547_1_sTW.root  DimuonSkim_88_1_yKX.root
DimuonSkim_241_1_YE6.root  DimuonSkim_395_1_MaQ.root  DimuonSkim_548_1_OEV.root  DimuonSkim_89_1_qnQ.root
DimuonSkim_242_1_Eh0.root  DimuonSkim_396_1_ouv.root  DimuonSkim_549_1_pDr.root  DimuonSkim_8_1_Yz3.root
DimuonSkim_243_1_ty1.root  DimuonSkim_397_1_yH5.root  DimuonSkim_54_1_0hm.root   DimuonSkim_90_1_zFC.root
DimuonSkim_244_1_Okb.root  DimuonSkim_398_1_H1h.root  DimuonSkim_550_1_uFw.root  DimuonSkim_91_1_glg.root
DimuonSkim_245_1_YlV.root  DimuonSkim_399_1_6Cg.root  DimuonSkim_551_1_Mhq.root  DimuonSkim_92_1_ZXe.root
DimuonSkim_246_1_F86.root  DimuonSkim_39_1_4kX.root   DimuonSkim_552_1_u0g.root  DimuonSkim_93_1_A94.root
DimuonSkim_247_1_Fpx.root  DimuonSkim_3_1_7ZH.root    DimuonSkim_553_1_IWV.root  DimuonSkim_94_1_Q76.root
DimuonSkim_248_1_iTc.root  DimuonSkim_400_1_pIT.root  DimuonSkim_554_1_6UL.root  DimuonSkim_95_1_MNw.root
DimuonSkim_249_1_yM0.root  DimuonSkim_401_1_sit.root  DimuonSkim_555_1_Sxa.root  DimuonSkim_96_1_8wJ.root
DimuonSkim_24_1_EON.root   DimuonSkim_402_1_b0q.root  DimuonSkim_556_1_a4D.root  DimuonSkim_97_1_l2C.root
DimuonSkim_250_1_WmY.root  DimuonSkim_403_1_tsE.root  DimuonSkim_557_1_7bm.root  DimuonSkim_98_1_L0f.root
DimuonSkim_251_1_Dfb.root  DimuonSkim_404_1_pOL.root  DimuonSkim_558_1_VEV.root  DimuonSkim_99_1_9C6.root
DimuonSkim_252_1_JK8.root  DimuonSkim_405_1_yak.root  DimuonSkim_559_1_Li8.root  DimuonSkim_9_1_qhW.root
DimuonSkim_253_1_AuM.root  DimuonSkim_406_1_SFn.root  DimuonSkim_55_1_zrn.root
""".split()
i = 7
process.source.fileNames = ["file:" + sourcePath + file for file in fileList[(i-1)*100:i*100] ]

process.output = cms.OutputModule("PoolOutputModule",
   fileName = cms.untracked.string("file:" + sourcePath + "MinimumBias_Commissioning10-CS_Onia-Jun14thSkim_v1_DimuonSkimPAT_%d.root" % i)
)

process.endpath = cms.EndPath(process.output)

