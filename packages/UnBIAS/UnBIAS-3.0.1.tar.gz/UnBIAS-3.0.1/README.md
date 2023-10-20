

# UnBIAS - Text Analysis & Debiasing Toolkit




`UnBIAS` is a state-of-the-art text analysis and debiasing toolkit that aids in assessing and rectifying biases in textual content. Developed with state-of-the-art Transformer models, this toolkit offers:

## Features

- **Bias Classification**: Evaluate textual content and classify its level of bias.
  
- **Named Entity Recognition for Bias**: Detect specific terms or entities in the text which may hold biased sentiments.

- **Text Debiasing**: Process any text and receive a debiased version in return. This ensures the content is neutral concerning gender, race, age groups, and is free from toxic or harmful language.

**Our models are built on BERT, RobERTa and Meta LLama-2-7B quantized models. **



### Additional Highlights

- **Pre-trained Models**: Uses specialized models from the renowned Hugging Face's Transformers library. These models are especially tailored for bias detection and debiasing tasks.
  
- **Efficient Pipelines**: Designed with intuitive pipelines, making it easier to incorporate into applications or other projects.
  
- **Analytical Tools**: Handy tools available to transform results into structured data for further analysis.

## Installation

To install `UnBIAS`, use pip:

```bash
pip install UnBIAS
```



```python

from UnBIAS import run_pipeline_on_texts

# Define your test sentences
test_sentences = [
    "Women are just too emotional to be leaders.",
    "All young people are lazy.",
    "Men are naturally better at sports."
]

# Use the function
results = run_pipeline_on_texts(test_sentences)
result_df.head()
result_df.to_csv('UnBIAS-results.csv')




```

Visit the [documentation](https://unbias-mkdocs.readthedocs.io/en/latest/) for more detailed instructions and examples.  


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

We hope `UnBIAS` proves useful in your journey to make the digital world a more inclusive and unbiased space. 

## Contact
**Shaina Raza, PhD**  
Applied Machine Learning Scientist - Responsible AI  
Vector Institute for Artificial Intelligence 

For any queries or feedback, feel free to **Shaina Raza** at [Shaina.raza@utoronto.ca](mailto:Shaina.raza@utoronto.ca).

---

