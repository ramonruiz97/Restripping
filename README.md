For now instrucitons are only for 2017


To re-run stripping:

On lxplus/Santiago (valid for 2017, for the rest of the years you have to adapt
DaVinci versions):

```
lb-set-platform x86_64-centos7-gcc62-opt
lb-dev DaVinci/v42r7p2
cd DaVinciDev_v42r7p2
git lb-use Stripping
git lb-checkout Stripping/2017-patches Phys/StrippingSelections
git lb-checkout Stripping/2017-patches Phys/StrippingSettings
```

Copy new stripping:

```
cd ..
scp stripping/StrippingB2JpsiXforBeta_s.py  DaVinciDev_v42r7p2/Phys/StrippingSelections/python/StrippingSelections/StrippingB2CC/StrippingB2JpsiXforBeta_s.py
scp stripping/LineConfigDictionaries_B2CC.py DaVinciDev_v42r7p2/Phys/StrippingSettings/python/StrippingSettings/Stripping29r2p2/LineConfigDictionaries_B2CC.py
make configure && make
```

Now for tuple maker we use same version for all years:
```
lb-set-platform x86_64_v2-centos7-gcc10-opt
lb-dev DaVinci/v45r8
cd DaVinciDev_v45r8
make configure
make
```


Then submit a job using ganga tasks - Don't forget to check the data sample - now uses only 2 lfns and is only for MD
```
ganga make_tuples.py {year} {polarity}
```
Data sample option is defined in `stripping/data_options.py`
And the restripping options are in `stripping/stripping_setup.py` 
Options for making the tuple are defined in `tuples/`
