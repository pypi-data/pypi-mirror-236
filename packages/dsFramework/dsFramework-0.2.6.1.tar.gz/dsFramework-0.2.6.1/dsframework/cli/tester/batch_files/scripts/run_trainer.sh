#!/bin/bash
# export GOOGLE_APPLICATION_CREDENTIALS=$GOOGLE_APPLICATION_CREDENTIALS
gcloud config set project dozi-data-science-research-1

rm -r ./build
rm -r ./dist
rm -r ./dsf_cloud_training.egg-info
bash ./batch_files/scripts/build_trainer.sh
dsf-cli upload-batch-files all

# python ./batch_files/workflow/auto_scaling_policy.py
python batch_files/workflow/workflow.py create_training
python batch_files/workflow/workflow.py instantiate

gcloud config set project dozi-stg-ds-apps-1
