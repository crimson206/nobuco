
phase1_example = '''
Generate simple inputs to run the target code block.

target:
```
torch.Tensor.add(*inputs)
```

output:
```python
inputs = [
    torch.randn(1, 20, 32),
    torch.randn(1, 20, 32)
]
```

'''

phase1_prompt = '''

<<Instruction>>

Given the context, complete the <<Task>>.

<<Documentation for {target}>>

{doc}

<<Example>>
{phase1_example}

<<Task>>
Generate simple inputs to run the target code block.

target:
```python
{target}
```

output:

'''