@echo off
set "TRAIN_FILE=project\training_data\ultra_corpus_n10\spacy_chunks_100000\file_train.spacy"
set "DEV_FILE=project\training_data\ultra_corpus_n10\spacy_chunks_100000\file_dev.spacy"
set "OUTPUT_DIR=project\models\specified_sk_model"

echo ==== Start ====
echo ...

echo ==== Training 1 ====
py -m spacy train project\models_cfg\idea_1.3.2\config_1.cfg --paths.train "%TRAIN_FILE%" --paths.dev "%DEV_FILE%" --output "%OUTPUT_DIR%"

echo ==== Training 2 ====
py -m spacy train project\models_cfg\idea_1.3.2\config_2.cfg --paths.train "%TRAIN_FILE%" --paths.dev "%DEV_FILE%" --output "%OUTPUT_DIR%"
 
echo ==== Training 3 ====
py -m spacy train project\models_cfg\idea_1.3.2\config_3.cfg --paths.train "%TRAIN_FILE%" --paths.dev "%DEV_FILE%" --output "%OUTPUT_DIR%"

echo ==== End of Training ====
pause
