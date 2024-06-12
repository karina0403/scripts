# prerequisite

## One-time run setup commands:
1. 
```
brew install virtualenv
```
2. 
```
virtualenv venv
```

## How to run the script
1. Activate python environment
```
source venv/bin/activate
```
2. Install required packages
```
pip install -r requirements.txt
```
3. Run the script with passing parameters:
```
python3 boot_volume_check.py \
--compartment_id <compartment_id> \
>> output_<compartment_name>.log
```

i.e.
```
python3 boot_volume_check.py \
--compartment_id ocid1.compartment.oc1..aaaaaaaa6pjlpqlirslme2lo675iyiqw73c345ekgpvfb6uwimtvruuazudq \
>> output_keenagi.log
```

4. Add optional parameters:
```
python3 boot_volume_check.py \
--profile <OCI_profile_name> \
--compartment_id <compartment_id> \
--verboose <True/False> \
>> output_<compartment_name>.log
```
i.e.
```
python3 boot_volume_check.py \
--profile CHICAGO \
--compartment_id ocid1.compartment.oc1..aaaaaaaa6pjlpqlirslme2lo675iyiqw73c345ekgpvfb6uwimtvruuazudq \
--verboose True \
>> output_keenagi.log
```
