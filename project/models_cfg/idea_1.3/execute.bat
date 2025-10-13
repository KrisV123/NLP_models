@echo off
set "TRAIN_FILE=project\training_data\ultra_corpus_n10\spacy_chunks_65000_hybrid\file_train.spacy"
set "TRAIN_2_FILE=project\training_data\ultra_corpus_n10\spacy_chunks_65000_hybrid\file_train_2.spacy"
set "DEV_FILE=project\training_data\ultra_corpus_n10\spacy_chunks_65000_hybrid\file_dev.spacy"
set "OUTPUT_DIR=project\models\full_sk_model_4"

echo ==== Start ====
echo ...

echo ==== Training 1 ====
py -m spacy train project\models_cfg\idea_1.3\config_1.cfg --paths.train "%TRAIN_2_FILE%" --paths.dev "%DEV_FILE%" --output "%OUTPUT_DIR%"

echo ==== Training 2 ====
py -m spacy train project\models_cfg\idea_1.3\config_2.cfg --paths.train "%TRAIN_FILE%" --paths.dev "%DEV_FILE%" --output "%OUTPUT_DIR%"
 
echo ==== Training 3 ====
py -m spacy train project\models_cfg\idea_1.3\config_3.cfg --paths.train "%TRAIN_FILE%" --paths.dev "%DEV_FILE%" --output "%OUTPUT_DIR%"

echo ==== End of Training ====
pause
