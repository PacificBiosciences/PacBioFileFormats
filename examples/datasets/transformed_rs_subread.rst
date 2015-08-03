Example Transformed_rs_subreadSet XML::

  <?xml version="1.0" encoding="UTF-8"?>
  <pbds:HdfSubreadSet xmlns:pbds="http://pacificbiosciences.com/PacBioDatasets.xsd"
                      UniqueId="ab772eb1-a553-44b0-83f6-716c22f41bb9"
                      TimeStampedName="hdfsubreadset_2015-08-03T12:20:11.032-08:00"
                      MetaType="PacBio.DataSet.SubreadSet"
                      Name="Subreads from runr000004_42268_150307"
                      Tags="pacbio.secondary.instrument=RS"
                      Version="0.5">
     <pbbase:ExternalResources xmlns:pbbase="http://pacificbiosciences.com/PacBioBaseDataModel.xsd">
        <pbbase:ExternalResource UniqueId="a5fe00f5-4938-415c-a2cc-ff31f3848bd2"
                                 TimeStampedName="hdfsubread_file_2015-08-03T12:20:11.032-08:00"
                                 MetaType="PacBio.SubreadFile.BaxFile"
                                 ResourceId="file:///C:/Users/aklammer/aklammer_laptop_2015/aklammer_laptop_2015/depot/software/smrtanalysis/bioinformatics/doc/FileFormats/examples/datasets/Analysis_Results/rs.1.bax.h5"/>
        <pbbase:ExternalResource UniqueId="a0625537-272e-4d0f-bcc9-41975576d083"
                                 TimeStampedName="hdfsubread_file_2015-08-03T12:20:11.032-08:00"
                                 MetaType="PacBio.SubreadFile.BaxFile"
                                 ResourceId="file:///C:/Users/aklammer/aklammer_laptop_2015/aklammer_laptop_2015/depot/software/smrtanalysis/bioinformatics/doc/FileFormats/examples/datasets/Analysis_Results/rs.2.bax.h5"/>
        <pbbase:ExternalResource UniqueId="a7c34ba1-b76b-4252-928e-bc0a379ed5a0"
                                 TimeStampedName="hdfsubreadset_file_2015-08-03T12:20:11.032-08:00"
                                 MetaType="PacBio.SubreadFile.BaxFile"
                                 ResourceId="file:///C:/Users/aklammer/aklammer_laptop_2015/aklammer_laptop_2015/depot/software/smrtanalysis/bioinformatics/doc/FileFormats/examples/datasets/Analysis_Results/rs.3.bax.h5"/>
     </pbbase:ExternalResources>
     <pbds:DataSetMetadata>
        <pbds:TotalLength>50000000</pbds:TotalLength>
        <pbds:NumRecords>150000</pbds:NumRecords>
        <pbmeta:Collections xmlns:pbmeta="http://pacificbiosciences.com/PacBioCollectionMetadata.xsd">
           <pbmeta:CollectionMetadata UniqueId="a5ab0791-b6be-422d-b96c-b0d8cc7e91e4"
                                      TimeStampedName="collection_metadata_2015-08-03T12:20:11.032-08:00"
                                      MetaType="PacBio.Collection"
                                      Context="rs"
                                      InstrumentName="42268"
                                      InstrumentId="1">
              <pbmeta:InstCtrlVer>2.3.0.1.142990</pbmeta:InstCtrlVer>
              <pbmeta:SigProcVer>NRT@172.31.128.10:8082, SwVer=2301.142990, HwVer=1.0</pbmeta:SigProcVer>
              <pbmeta:RunDetails xmlns:uuid="java:java.util.UUID"
                                 xmlns="http://pacificbiosciences.com/PacBioDataModel.xsd"
                                 xmlns:xs="http://www.w3.org/2001/XMLSchema"
                                 xmlns:bax="http://whatever"
                                 xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                                 xmlns:pbbase="http://pacificbiosciences.com/PacBioBaseDataModel.xsd"
                                 xmlns:pbsample="http://pacificbiosciences.com/PacBioSampleInfo.xsd"
                                 xmlns:fn="http://www.w3.org/2005/xpath-functions"
                                 xmlns:pbsec="http://pacificbiosciences.com/PacBioSecondaryDataModel.xsd">
                 <pbmeta:RunId>r000004_42268_150307</pbmeta:RunId>
                 <pbmeta:Name>Inst42268-030715-2kb-P4-0.05nM-6Chips-FAT2_3</pbmeta:Name>
              </pbmeta:RunDetails>
              <pbmeta:WellSample Name="Inst42268-030715-2kb-P4-0.05nM-2Chips-FAT3">
                 <pbmeta:PlateId>Inst42268-030715-2kb-P4-0.05nM-6Chips-FAT2_3</pbmeta:PlateId>
                 <pbmeta:WellName>Inst42268-030715-2kb-P4-0.05nM-2Chips-FAT3</pbmeta:WellName>
                 <pbmeta:Concentration>0</pbmeta:Concentration>
                 <pbmeta:SampleReuseEnabled>false</pbmeta:SampleReuseEnabled>
                 <pbmeta:StageHotstartEnabled>true</pbmeta:StageHotstartEnabled>
                 <pbmeta:SizeSelectionEnabled>
                                  false
                              </pbmeta:SizeSelectionEnabled>
                 <pbmeta:UseCount>1</pbmeta:UseCount>
                 <pbsample:BioSamplePointers xmlns:pbsample="http://pacificbiosciences.com/PacBioSampleInfo.xsd">
                    <pbsample:BioSamplePointer>a6a7687e-4733-4695-adb0-1542d84b75c8</pbsample:BioSamplePointer>
                 </pbsample:BioSamplePointers>
              </pbmeta:WellSample>
              <pbmeta:Automation>
                 <pbbase:AutomationParameters xmlns:pbbase="http://pacificbiosciences.com/PacBioBaseDataModel.xsd">
                    <pbbase:AutomationParameter/>
                 </pbbase:AutomationParameters>
              </pbmeta:Automation>
              <pbmeta:CollectionNumber>6</pbmeta:CollectionNumber>
              <pbmeta:CellIndex>1</pbmeta:CellIndex>
              <pbmeta:CellPac Barcode="10078306255000000182317020825155"/>
              <pbmeta:Primary>
                 <pbmeta:AutomationName>BasecallerV1</pbmeta:AutomationName>
                 <pbmeta:ConfigFileName>2-0-0_P4-C2.xml</pbmeta:ConfigFileName>
                 <pbmeta:SequencingCondition/>
                 <pbmeta:OutputOptions>
                    <pbmeta:ResultsFolder>Analysis_Results</pbmeta:ResultsFolder>
                    <pbmeta:CollectionPathUri>rsy://mp-rsync/vol55//RS_DATA_STAGING/42268/Inst42268-030715-2kb-P4-0.05nM-6Chips-FAT2_3_4/B01_2/</pbmeta:CollectionPathUri>
                    <pbmeta:CopyFiles>
                       <pbmeta:CollectionFileCopy>Fasta</pbmeta:CollectionFileCopy>
                    </pbmeta:CopyFiles>
                    <pbmeta:Readout>Bases</pbmeta:Readout>
                    <pbmeta:MetricsVerbosity>Minimal</pbmeta:MetricsVerbosity>
                 </pbmeta:OutputOptions>
              </pbmeta:Primary>
           </pbmeta:CollectionMetadata>
        </pbmeta:Collections>
        <pbsample:BioSamples xmlns:pbsample="http://pacificbiosciences.com/PacBioSampleInfo.xsd">
           <pbsample:BioSample UniqueId="a6a7687e-4733-4695-adb0-1542d84b75c8"
                               TimeStampedName="biosample_2015-08-03T12:20:11.032-08:00"
                               MetaType="PacBio.Sample"
                               Name="Inst42268-030715-2kb-P4-0.05nM-2Chips-FAT3"
                               Description="Inst42268-030715-2kb-P4-0.05nM-2Chips-FAT3"/>
        </pbsample:BioSamples>
     </pbds:DataSetMetadata>
  </pbds:HdfSubreadSet>