#
Copyright 2016 Google Inc.All Rights Reserved.Licensed under the Apache# License, Version 2.0(the "License");
you may not use this file except in #compliance with the License.You may obtain a copy of the License at# http: //www.apache.org/licenses/LICENSE-2.0

        #Unless required by applicable law or agreed to in writing, software# distributed under the License is distributed on an "AS IS"
BASIS, WITHOUT# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.See the# License
for the specific language governing permissions and limitations under# the License.

""
"Define a Wide + Deep model for classification on structured data."
""

from __future__
import absolute_import
from __future__
import division
from __future__
import print_function

import multiprocessing

import six
import tensorflow as tf

# Define the format of your input data including unused columns# CSV_COLUMNS = ['age', 'workclass', 'fnlwgt', 'education', 'education_num', #'marital_status', 'occupation', 'relationship', 'race', 'gender', #'capital_gain', 'capital_loss', 'hours_per_week', #'native_country', 'income_bracket']

CSV_COLUMNS = ['Global.Variance', 'Global.Skewness', 'Global.Kurtosis', 'GLCM.Energy', 'GLCM.Contrast', 'GLCM.Entropy', 'GLCM.Homogeneity', 'GLCM.Correlation',
        'GLCM.SumAverage', 'GLCM.Variance', 'GLCM.Dissimilarity', 'GLCM.AutoCorrelation', 'GLRLM.SRE', 'GLRLM.LRE', 'GLRLM.GLN', 'GLRLM.RLN', 'GLRLM.RP', 'GLRLM.LGRE', 'GLRLM.HGRE',
        'GLRLM.SRLGE', 'GLRLM.SRHGE', 'GLRLM.LRLGE', 'GLRLM.LRHGE', 'GLRLM.GLV', 'GLRLM.RLV', 'GLSZM.SZE', 'GLSZM.LZE', 'GLSZM.GLN', 'GLSZM.ZSN', 'GLSZM.ZP', 'GLSZM.LGZE', 'GLSZM.HGZE', 'GLSZM.SZLGE',
        'GLSZM.SZHGE', 'GLSZM.LZLGE', 'GLSZM.LZHGE', 'GLSZM.GLV', 'GLSZM.ZSV', 'NGTDM.Coarseness', 'NGTDM.Contrast', 'NGTDM.Busyness', 'NGTDM.Complexity', 'NGTDM.Strength', 'Mets'
]
CSV_COLUMN_DEFAULTS = [
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0],
        [0]
]

# LABEL_COLUMN = 'income_bracket'#
LABELS = [' <=50K', ' >50K']
LABEL_COLUMN = 'Mets'
LABELS = ['0', '1']

# Define the initial ingestion of each feature used by your model.#Additionally, provide metadata about the feature.
INPUT_COLUMNS = [#Categorical base columns

        # For categorical columns with known values we can provide lists# of values ahead of time.#tf.feature_column.categorical_column_with_vocabulary_list(#'gender', [' Female', ' Male']),

        #tf.feature_column.categorical_column_with_vocabulary_list(#'race', # [' Amer-Indian-Eskimo', ' Asian-Pac-Islander', #' Black', ' Other', ' White']#), #tf.feature_column.categorical_column_with_vocabulary_list(#'education', # [' Bachelors', ' HS-grad', ' 11th', ' Masters', ' 9th', #' Some-college', ' Assoc-acdm', ' Assoc-voc', ' 7th-8th', #' Doctorate', ' Prof-school', ' 5th-6th', ' 10th', #' 1st-4th', ' Preschool', ' 12th']), #tf.feature_column.categorical_column_with_vocabulary_list(#'marital_status', # [' Married-civ-spouse', ' Divorced', ' Married-spouse-absent', #' Never-married', ' Separated', ' Married-AF-spouse', ' Widowed']), #tf.feature_column.categorical_column_with_vocabulary_list(#'relationship', # [' Husband', ' Not-in-family', ' Wife', ' Own-child', ' Unmarried', #' Other-relative']), #tf.feature_column.categorical_column_with_vocabulary_list(#'workclass', # [' Self-emp-not-inc', ' Private', ' State-gov', #' Federal-gov', ' Local-gov', ' ?', ' Self-emp-inc', #' Without-pay', ' Never-worked']#),

        #For columns with a large number of values, or unknown values# We can use a hash
        function to convert to categories.#tf.feature_column.categorical_column_with_hash_bucket(#'occupation', hash_bucket_size = 100, dtype = tf.string), #tf.feature_column.categorical_column_with_hash_bucket(

                #'native_country', hash_bucket_size = 100, dtype = tf.string),

        #Continuous base columns.
        tf.feature_column.numeric_column('Global.Variance'),
        tf.feature_column.numeric_column('Global.Skewness'),
        tf.feature_column.numeric_column('Global.Kurtosis'),
        tf.feature_column.numeric_column('GLCM.Energy'),
        tf.feature_column.numeric_column('GLCM.Contrast'),
        tf.feature_column.numeric_column('GLCM.Entropy'),
        tf.feature_column.numeric_column('GLCM.Homogeneity'),
        tf.feature_column.numeric_column('GLCM.Correlation'),
        tf.feature_column.numeric_column('GLCM.SumAverage'),
        tf.feature_column.numeric_column('GLCM.Variance'),
        tf.feature_column.numeric_column('GLCM.Dissimilarity'),
        tf.feature_column.numeric_column('GLCM.AutoCorrelation'),
        tf.feature_column.numeric_column('GLRLM.SRE'),
        tf.feature_column.numeric_column('GLRLM.LRE'),
        tf.feature_column.numeric_column('GLRLM.GLN'),
        tf.feature_column.numeric_column('GLRLM.RLN'),
        tf.feature_column.numeric_column('GLRLM.RP'),
        tf.feature_column.numeric_column('GLRLM.LGRE'),
        tf.feature_column.numeric_column('GLRLM.HGRE'),
        tf.feature_column.numeric_column('GLRLM.SRLGE'),
        tf.feature_column.numeric_column('GLRLM.SRHGE'),
        tf.feature_column.numeric_column('GLRLM.LRLGE'),
        tf.feature_column.numeric_column('GLRLM.GLV'),
        tf.feature_column.numeric_column('GLRLM.RLV'),
        tf.feature_column.numeric_column('GLSZM.SZE'),
        tf.feature_column.numeric_column('GLSZM.LZE'),
        tf.feature_column.numeric_column('GLSZM.GLN'),
        tf.feature_column.numeric_column('GLSZM.ZSN'),
        tf.feature_column.numeric_column('GLSZM.ZP'),
        tf.feature_column.numeric_column('GLSZM.LGZE'),
        tf.feature_column.numeric_column('GLSZM.HGZE'),
        tf.feature_column.numeric_column('GLSZM.SZLGE'),
        tf.feature_column.numeric_column('GLSZM.SZHGE'),
        tf.feature_column.numeric_column('GLSZM.LZLGE'),
        tf.feature_column.numeric_column('GLSZM.LZHGE'),
        tf.feature_column.numeric_column('GLSZM.GLV'),
        tf.feature_column.numeric_column('GLSZM.ZSV'),
        tf.feature_column.numeric_column('NGTDM.Coarseness'),
        tf.feature_column.numeric_column('NGTDM.Contrast'),
        tf.feature_column.numeric_column('NGTDM.Busyness'),
        tf.feature_column.numeric_column('NGTDM.Complexity'),
        tf.feature_column.numeric_column('NGTDM.Strength'),
        tf.feature_column.numeric_column('Mets')

]

UNUSED_COLUMNS = set(CSV_COLUMNS) - {
        col.name
        for col in INPUT_COLUMNS
} - \{
        LABEL_COLUMN
}

def build_estimator(config, embedding_size = 8, hidden_units = None):

        (Global.Variance, Global.Skewness, Global.Kurtosis, GLCM.Energy, GLCM.Contrast, GLCM.Entropy, GLCM.Homogeneity,
                GLCM.Correlation, GLCM.SumAverage, GLCM.Variance, GLCM.Dissimilarity, GLCM.AutoCorrelation, GLRLM.SRE, GLRLM.LRE, GLRLM.GLN,
                GLRLM.RLN, GLRLM.RP, GLRLM.LGRE, GLRLM.HGRE, GLRLM.SRLGE, GLRLM.SRHGE, GLRLM.LRLGE, GLRLM.LRHGE, GLRLM.GLV, GLRLM.RLV,
                GLSZM.SZE, GLSZM.LZE, GLSZM.GLN, GLSZM.ZSN, GLSZM.ZP, GLSZM.LGZE, GLSZM.HGZE, GLSZM.SZLGE, GLSZM.SZHGE, GLSZM.LZLGE,
                GLSZM.LZHGE, GLSZM.GLV, GLSZM.ZSV, NGTDM.Coarseness, NGTDM.Contrast, NGTDM.Busyness, NGTDM.Complexity,
                NGTDM.Strength) = INPUT_COLUMNS

wide_columns = [
        Global.Variance,
        Global.Skewness,
        Global.Kurtosis,
        GLCM.Energy,
        GLCM.Contrast,
        GLCM.Entropy,
        GLCM.Homogeneity,
        GLCM.Correlation,
        GLCM.SumAverage,
        GLCM.Variance,
        GLCM.Dissimilarity,
        GLCM.AutoCorrelation,
]

deep_columns = [
        GLRLM.SRE,
        GLRLM.LRE,
        GLRLM.GLN,
        GLRLM.RLN,
        GLRLM.RP,
        GLRLM.LGRE,
        GLRLM.HGRE,
        GLRLM.SRLGE,
        GLRLM.SRHGE,
        GLRLM.LRLGE,
        GLRLM.LRHGE,
        GLRLM.GLV,
        GLRLM.RLV,
        GLSZM.SZE,
        GLSZM.LZE,
        GLSZM.GLN,
        GLSZM.ZSN,
        GLSZM.ZP,
        GLSZM.LGZE,
        GLSZM.HGZE,
        GLSZM.SZLGE,
        GLSZM.SZHGE,
        GLSZM.LZLGE,
        GLSZM.LZHGE,
        GLSZM.GLV,
        GLSZM.ZSV,
        NGTDM.Coarseness,
        NGTDM.Contrast,
        NGTDM.Busyness,
        NGTDM.Complexity,
        NGTDM.Strength,
]

return tf.estimator.DNNLinearCombinedClassifier(
        config = config,
        linear_feature_columns = wide_columns,
        dnn_feature_columns = deep_columns,
        dnn_hidden_units = hidden_units or[100, 70, 50, 25]
)

def parse_label_column(label_string_tensor):
        ""
"Parses a string tensor into the label tensor
Args:
        label_string_tensor: Tensor of dtype string.Result of parsing the
CSV column specified by LABEL_COLUMN
Returns:
        A Tensor of the same shape as label_string_tensor, should
return
an int64 Tensor representing the label index
for classification tasks,
and a float32 Tensor representing the value
for a regression task.
""
"#
Build a Hash Table inside the graph
table = tf.contrib.lookup.index_table_from_tensor(tf.constant(LABELS))

# Use the hash table to convert string labels to ints and one - hot encode
return table.lookup(label_string_tensor)

# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * #YOU NEED NOT MODIFY ANYTHING BELOW HERE TO ADAPT THIS MODEL TO YOUR DATA# * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *

        def csv_serving_input_fn():
        ""
"Build the serving inputs."
""
csv_row = tf.placeholder(
        shape = [None],
        dtype = tf.string
)
features = parse_csv(csv_row)
features.pop(LABEL_COLUMN)
return tf.estimator.export.ServingInputReceiver(features, {
        'csv_row': csv_row
})

def example_serving_input_fn():
        ""
"Build the serving inputs."
""
example_bytestring = tf.placeholder(
        shape = [None],
        dtype = tf.string,
)
feature_scalars = tf.parse_example(
        example_bytestring,
        tf.feature_column.make_parse_example_spec(INPUT_COLUMNS)
)
return tf.estimator.export.ServingInputReceiver(
        features, {
                'example_proto': example_bytestring
        }
)

#[START serving - function]
def json_serving_input_fn():
        ""
"Build the serving inputs."
""
inputs = {}
for feat in INPUT_COLUMNS:
        inputs[feat.name] = tf.placeholder(shape = [None], dtype = feat.dtype)

return tf.estimator.export.ServingInputReceiver(inputs, inputs)#[END serving - function]

SERVING_FUNCTIONS = {
        'JSON': json_serving_input_fn,
        'EXAMPLE': example_serving_input_fn,
        'CSV': csv_serving_input_fn
}

def parse_csv(rows_string_tensor):
        ""
"Takes the string input tensor and returns a dict of rank-2 tensors."
""

#
Takes a rank - 1 tensor and converts it into rank - 2 tensor# Example
if the data is['csv,line,1', 'csv,line,2', ..] to#[['csv,line,1'], ['csv,line,2']] which after parsing will result in a# tuple of tensors: [
        ['csv'],
        ['csv']
], [
        ['line'],
        ['line']
], [
        [1],
        [2]
]
row_columns = tf.expand_dims(rows_string_tensor, -1)
columns = tf.decode_csv(row_columns, record_defaults = CSV_COLUMN_DEFAULTS)
features = dict(zip(CSV_COLUMNS, columns))

# Remove unused columns
for col in UNUSED_COLUMNS:
        features.pop(col)
return features

def input_fn(filenames,
                num_epochs = None,
                shuffle = True,
                skip_header_lines = 0,
                batch_size = 200):
        ""
"Generates features and labels for training or evaluation.
This uses the input pipeline based approach using file name queue
to read data so that entire data is not loaded in memory.

Args:
        filenames: [str] list of CSV files to read data from.
num_epochs: int how many times through to read the data.
If None will loop through data indefinitely
shuffle: bool, whether or not to randomize the order of data.
Controls randomization of both file order and line order within
files.
skip_header_lines: int set to non - zero in order to skip header lines in CSV files.
batch_size: int First dimension size of the Tensors returned by
input_fn
Returns:
        A(features, indices) tuple where features is a dictionary of
Tensors, and indices is a single Tensor of label indices.
""
"
filename_dataset = tf.data.Dataset.from_tensor_slices(filenames)
if shuffle: #Process the files in a random order.
filename_dataset = filename_dataset.shuffle(len(filenames))

# For each filename, parse it into one element per line, and skip the header#
if necessary.
dataset = filename_dataset.flat_map(
        lambda filename: tf.data.TextLineDataset(filename).skip(skip_header_lines))

dataset = dataset.map(parse_csv)
if shuffle:
        dataset = dataset.shuffle(buffer_size = batch_size * 10)
dataset = dataset.repeat(num_epochs)
dataset = dataset.batch(batch_size)
iterator = dataset.make_one_shot_iterator()
features = iterator.get_next()
return features, parse_label_column(features.pop(LABEL_COLUMN))
