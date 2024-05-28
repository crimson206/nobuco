
import unittest
import torch
import nobuco
import torch.nn as nn
import torch.nn.functional as F


class TestAutogenatedUnittests(unittest.TestCase):
    
    def test_F_one_hot_converter(self):
        # Initialize the model directly from its constructor
    
        class MyModule(torch.nn.Module):
            def __init__(self):
                super().__init__()
    
            def forward(self, inputs):
                F.one_hot(*inputs)
    
        torch_model = MyModule()
    
        torch_model.eval()
    	# Initialize the model and input tensor
        inputs = [
        torch.arange(0, 5) % 3,
        torch.arange(0, 6).view(3, 2)) % 3
    
    
    ]
    
        # Convert the model and ensure the HTML trace is saved
        keras_model = nobuco.pytorch_to_keras(
            torch_model,
            args = [inputs], kwargs = None,
            inputs_channel_order = nobuco.ChannelOrder.TENSORFLOW,
            outputs_channel_order = nobuco.ChannelOrder.TENSORFLOW,
            save_trace_html = True
        )
    
        # Read the contents of the trace.html file
        with open('trace.html', 'r', encoding='utf-8') as file:
            trace_html = file.read()
    
        # Assertions for the content of trace_html
        self.assertNotIn('Max diff', trace_html, "The trace HTML should not contain 'Max diff'")
    
if __name__ == '__main__':
    unittest.main()

