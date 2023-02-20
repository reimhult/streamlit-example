# -*- coding: utf-8 -*-
"""
Created on Wed Dec 29 13:42:12 2021

@author: Daniel
"""

import numpy as np
import pandas as pd
import streamlit as st
import altair as alt

hide_decoration_bar_style = '''
    <style>
        header {visibility: hidden;}
    </style>
'''
st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

st.header('Input signal')

frequency = st.slider('Frequency (Hz)', min_value=1, max_value=100, value=10)
input_sample_rate = st.slider('Sample rate (Hz)', min_value=10, max_value=1000, value=200)

num_seconds = 1
num_samples = num_seconds * input_sample_rate

upsampling_rate = 2
downsampling_rate = 5

spectral_components = [{'frequency': frequency, 'amplitude': 1, 'phase': 0}]

time = np.arange(num_samples) / input_sample_rate

output_sample_rate = input_sample_rate * upsampling_rate // downsampling_rate

input_signal = np.zeros(num_samples)

for sc in spectral_components:
    input_signal += sc['amplitude'] * np.sin( 2*np.pi*sc['frequency']*time + sc['phase'] * np.pi / 180.0 )

df_input = pd.DataFrame({'Input signal': input_signal, 'time': time})

input_chart = alt.Chart(df_input).mark_line().encode(
    x='time',
    y='Input signal'
)    

st.altair_chart(input_chart, use_container_width=True)

input_spectrum = np.abs(np.fft.fft(input_signal))[:num_samples//2] / (num_samples//2)
frequencies = np.fft.fftfreq(num_samples, 1 / input_sample_rate)[:num_samples//2]

df_spectrum = pd.DataFrame({'Amplitude spectrum': input_spectrum, 'Frequency (Hz)': frequencies})

spectrum_chart = alt.Chart(df_spectrum).mark_line().encode(
    x='Frequency (Hz)',
    y='Amplitude spectrum'
)    

st.altair_chart(spectrum_chart, use_container_width=True)

max_index = np.argmax(input_spectrum)
det_freq = frequencies[max_index]

st.text(f'Input signal frequency: {frequency:.2f} Hz')
st.text(f'Detected frequency: {det_freq:.2f} Hz')

