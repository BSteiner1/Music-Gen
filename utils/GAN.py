#------------------------------------------------------------------------------------------------------------------------------------

# Define the Generator and Discriminator networks
class Generator(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers):
        super(Generator, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # Define the LSTM layers
        self.lstm = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)

        # Add 3 fully connected layers
        self.fc1 = nn.Linear(hidden_dim, 80)  
        self.fc2 = nn.Linear(80, 64)  
        self.fc3 = nn.Linear(64, 32)  

        # Sigmoid activation
        self.sigmoid = nn.Sigmoid()

        # ReLU activation
        self.ReLU = nn.ReLU()
        
        # Dropout 
        self.Dropout = nn.Dropout(0.3)

    def forward(self, x):
        batch_size = x.size(0)
        seq_length = x.size(1)

        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(x.device)

        out, _ = self.lstm(x, (h0, c0))

        # Pass LSTM output through 3 FC layers with ReLU activation
        out = self.fc1(out)
        out = self.ReLU(out)
        out = self.Dropout(out)
        out = self.fc2(out)
        out = self.ReLU(out)
        out = self.Dropout(out)
        out = self.fc3(out) 
        out = self.ReLU(out)
        out = self.Dropout(out)

        # Apply sigmoid activation to squash the values between 0 and 1
        # Then scale to the range [0, 128]
        out = torch.sigmoid(out) * 128  

        return out
    
#------------------------------------------------------------------------------------------------------------------------------------

class Discriminator(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim, num_layers):
        super(Discriminator, self).__init__()
        self.hidden_dim = hidden_dim
        self.num_layers = num_layers

        # LSTM layers
        self.lstm = nn.LSTM(input_size=input_dim, hidden_size=hidden_dim, num_layers=num_layers, batch_first=True)

        # FC layers
        self.fc1 = nn.Linear(hidden_dim, 80)  
        self.fc2 = nn.Linear(80, 64)  
        self.fc3 = nn.Linear(64, output_dim)  

        # ReLU activation
        self.ReLU = nn.ReLU()
        
        # Dropout 
        self.Dropout = nn.Dropout(0.3)

    def forward(self, x):
        batch_size = x.size(0)
        h0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(x.device)
        c0 = torch.zeros(self.num_layers, batch_size, self.hidden_dim).to(x.device)

        out, _ = self.lstm(x, (h0, c0))

        # Apply the FC layers, activations, and Dropout to LSTM output
        out = self.fc1(out[:, -1, :])
        out = self.ReLU(out)
        out = self.Dropout(out)
        out = self.fc2(out)
        out = self.ReLU(out)
        out = self.Dropout(out)
        out = self.fc3(out) 
        out = self.ReLU(out)
        out = self.Dropout(out)

        return out  
    
#------------------------------------------------------------------------------------------------------------------------------------

class LSTMGAN(nn.Module):
    def __init__(self, input_dim, generator_input_dim, discriminator_input_dim, hidden_dim, num_layers):
        super(LSTMGAN, self).__init__()
        self.input_dim = input_dim
        self.generator = Generator(generator_input_dim, hidden_dim, input_dim, num_layers)
        self.discriminator = Discriminator(discriminator_input_dim, hidden_dim, 1, num_layers)

    def train(self, data_loader, epochs):
        self.generator
        self.discriminator

        criterion = nn.BCEWithLogitsLoss()
        g_optimizer = torch.optim.Adam(self.generator.parameters(), lr=0.0001)
        d_optimizer = torch.optim.Adam(self.discriminator.parameters(), lr=0.001)

        for epoch in range(epochs):
            d_loss_sum = 0.0
            g_loss_sum = 0.0

            for batch in data_loader:  
                real_data = batch

                batch_size = real_data.size(0)  
                real_labels = torch.ones(batch_size, 1).long()
                fake_labels = torch.zeros(batch_size, 1).long()

                d_optimizer.zero_grad()
                real_labels = torch.ones(batch_size, 1).long()
                fake_labels = torch.zeros(batch_size, 1).long()

                noise = torch.randn(batch_size, 4, generator_input_dim)
                fake_data = self.generator(noise)

                real_data = real_data.view(batch_size, 4, input_dim)
                real_outputs = self.discriminator(real_data)

                fake_outputs = self.discriminator(fake_data.detach())

                real_outputs = real_outputs.view(batch_size, -1)
                fake_outputs = fake_outputs.view(batch_size, -1)

                d_real_loss = criterion(real_outputs, real_labels.float())
                d_fake_loss = criterion(fake_outputs, fake_labels.float())

                d_loss = d_real_loss + d_fake_loss
                d_loss.backward()
                d_optimizer.step()

                g_optimizer.zero_grad()
                noise = torch.randn(batch_size, 4, generator_input_dim)#.to(device)
                fake_data = self.generator(noise)
                fake_data = fake_data.view(batch_size, 4, input_dim)
                fake_outputs = self.discriminator(fake_data)

                fake_outputs = fake_outputs.view(batch_size, -1)

                g_loss = criterion(fake_outputs, fake_labels.float())
                g_loss.backward()
                g_optimizer.step()

                d_loss_sum += d_loss.item()
                g_loss_sum += g_loss.item()

            # Calculate the average loss for this epoch
            avg_d_loss = d_loss_sum / len(data_loader)
            avg_g_loss = g_loss_sum / len(data_loader)

            print(f"Epoch {epoch + 1}/{epochs}, D Loss: {avg_d_loss}, G Loss: {avg_g_loss}")
            
#------------------------------------------------------------------------------------------------------------------------------------

class MyDataset(data):
    """
    A class to build a dataloader
    
    Args:
        - data (list): A list of the arrays
        
    Returns:
        - A dataset that can be converted into a PyTorch dataloader
    """

    def __init__(self, data):
        self.data = data 

    def __len__(self):
        return len(self.data)

    def __getitem__(self, idx):
        sample = self.data[idx]
        return sample
    
#------------------------------------------------------------------------------------------------------------------------------------