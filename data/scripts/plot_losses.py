import pandas as pd
import matplotlib.pyplot as plt

# Load the losses from the CSV file
df_losses = pd.read_csv("training_losses.csv")

# Calculate the total loss
VEL_LOSS_LAMBDA = 10.0
if 'Onset_Loss' in df_losses.columns:
    df_losses['Total_Loss'] = df_losses['Onset_Loss'] + VEL_LOSS_LAMBDA * df_losses['Velocity_Loss']
else:
    # If there is no onset loss recorded, total loss is just the velocity loss
    df_losses['Total_Loss'] = df_losses['Velocity_Loss']

# Plot the velocity loss
plt.figure(figsize=(10, 5))
plt.plot(df_losses['Step'], df_losses['Velocity_Loss'], label='Velocity Loss')

# Plot the onset loss if it exists
if 'Onset_Loss' in df_losses.columns:
    plt.plot(df_losses['Step'], df_losses['Onset_Loss'], label='Onset Loss')

# Plot the total loss
plt.plot(df_losses['Step'], df_losses['Total_Loss'], label='Total Loss')

plt.title('Training Losses Over Steps')
plt.xlabel('Step')
plt.ylabel('Loss')
plt.legend()
plt.show()
