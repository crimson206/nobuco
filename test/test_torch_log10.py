
import unittest
import torch
import nobuco
import torch.nn as nn
import torch.nn.functional as F


class TestAutogenatedUnittests(unittest.TestCase):
    
    def test_torch_log10_converter(self):
        # Initialize the model directly from its constructor
    
        class MyModule(torch.nn.Module):
            def __init__(self):
                super().__init__()
    
            def forward(self, inputs):
                torch.log10(*inputs)
    
        torch_model = MyModule()
    
        torch_model.eval()
        # Initialize the model and input tensor
        inputs = [
            torch.tensor([1000.], dtype=torch.float64)
        ]
    
        # Convert the model and ensure the HTML trace is saved
        keras_model = nobuco.pytorch_to_keras(
            torch_model,
            args=[inputs], kwargs=None,
            inputs_channel_order=nobuco.ChannelOrder.TENSORFLOW,
            outputs_channel_order=nobuco.ChannelOrder.TENSORFLOW,
            save_trace_html=True
        )
    
        # Read the contents of the trace.html file
        with open('trace.html', 'r', encoding='utf-8') as file:
            trace_html = file.read()
    
        # Assertions for the content of trace_html
        self.assertNotIn('Max diff', trace_html,
                         "The trace HTML should not contain 'Max diff'")
    
if __name__ == '__main__':
    unittest.main()

