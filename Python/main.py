#  ____  ____      _    __  __  ____ ___
# |  _ \|  _ \    / \  |  \/  |/ ___/ _ \
# | | | | |_) |  / _ \ | |\/| | |  | | | |
# | |_| |  _ <  / ___ \| |  | | |__| |_| |
# |____/|_| \_\/_/   \_\_|  |_|\____\___/
#                           research group
#                             dramco.be/
#
#  KU Leuven - Technology Campus Gent,
#  Gebroeders De Smetstraat 1,
#  B-9000 Gent, Belgium
#
#         File: main.py
#      Created: 09-07-2021
#       Author: Chesney Buyle
#      Version: 1.0
#
#  Description: Phased Array Measurements
#      Array calibration: amplitude and phase
#      Beam pattern measurements

from controller import *
from daq import *
from stepper import *
import time
import keyboard
from scipy.optimize import curve_fit

devices = [0x03, 0x01, 0x0B, 0x0A, 0x07, 0x05, 0x0F, 0x0D, 0x02, 0x08]
frequencies = [10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000, 21000, 22000, 23000, 24000,
               25000, 26000, 27000, 28000, 29000, 30000, 31000, 32000, 33000, 34000, 35000]
# frequencies = [31000, 32000]

default_rpot = 12000

# Amplitude calibration settings
db_rms_deviation = 0.5  # dB

# Phase calibration settings
min_phase_calibration = -140
max_phase_calibration = 140
phase_calibration_step = 5

sleep_time_after_speaker_change = 0.2

steering_angle = 70

current_angle_az = 0
turn_degree_az = 1
total_turns_one_revolution_from_angle_az = round(360 / turn_degree_az)
total_turns_one_revolution_from_angle_el = 1
rms_vs_angle = np.zeros((total_turns_one_revolution_from_angle_el, total_turns_one_revolution_from_angle_az))

array_configuration = "1x10"
freq = "25kHz"
dist = "0_75m"
beam_angle = "0"

# Data files
version = "anechoic"
f_name_uncalibrated_speaker_sweep = "uncal_speaker_sweep_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_min = "uncal_speaker_sweep_min_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_max = "uncal_speaker_sweep_max_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_std = "uncal_speaker_sweep_std_" + version + ".txt"
f_name_uncalibrated_speaker_sweep_info = "uncal_speaker_sweep_info_" + version + ".txt"

f_name_calibrated_speaker_sweep = "cal_speaker_sweep_" + version + ".txt"
f_name_calibrated_speaker_sweep_min = "cal_speaker_sweep_min_" + version + ".txt"
f_name_calibrated_speaker_sweep_max = "cal_speaker_sweep_max_" + version + ".txt"
f_name_calibrated_speaker_sweep_std = "cal_speaker_sweep_std_" + version + ".txt"
f_name_calibrated_speaker_sweep_info = "cal_speaker_sweep_info_" + version + ".txt"

f_name_calibrated_rpot = "calibrated_rpot_" + version + ".txt"
f_name_error_file_response_calibration = "error_" + version + ".txt"

f_name_calibrated_phase_shifts = "calibrated_phase_shifts_" + version + ".txt"
f_name_calibrated_phase_shifts_info = "calibrated_phase_shifts_info_" + version + ".txt"

f_name_beam_pattern_base = "beampattern_" + str(array_configuration) + "_config_" + str(freq) + "_" + str(dist) + \
                           "_beamangle_" + str(beam_angle) + "_" + str(version)


# First, let's calibrate the speaker array
# Step 1: amplitude calibration
# Step 2: phase calibration

# Amplitude calibration
# First, we measure the responses of the speaker elements over a certain frequency range
# The speaker with the lowest response at a certain frequency is used as reference
# and all speakers are amplitude calibrated towards the same response


def calibrate_amplitude():
    # Step 1: measure speaker responses
    measure_frequency_response()

    # Step 2: calibrate speaker responses
    calibrate_speaker_responses()

    # Step 3: sweep calibrated speaker responses
    measure_calibrated_frequency_response()


def calibrate_phase():
    # Step 1: measure phase offset w.r.t. speaker 0
    measure_phase_offsets()

    # Step 2: apply fitting to calculate the phase offsets
    calculate_phase_offsets()


def measure_phase_offsets():
    global f_name_calibrated_speaker_sweep_info
    global f_name_calibrated_speaker_sweep
    global sleep_time_after_speaker_change
    global version
    global min_phase_calibration
    global max_phase_calibration
    global phase_calibration_step

    # Speaker 0 is used as reference speaker
    # The other speakers are enabled one by one separately and the phase is shifted between [0° and 360°]
    # The resulting response should be a sine wave, and the phase offset is calculated through fitting

    # First, we read the info data from the amplitude calibration measurements
    f_info = open(f_name_calibrated_speaker_sweep_info, "r")
    str_devices = f_info.readline().rstrip('\n').lstrip("devices: ").replace(" ", "")
    l_devices = np.array(str_devices.split(",")).astype(np.ushort)
    print(l_devices)
    str_frequencies = f_info.readline().rstrip('\n').lstrip("frequencies: ").replace(" ", "")
    l_frequencies = np.array(str_frequencies.split(",")).astype(np.ushort)
    print(l_frequencies)
    f_info.close()

    # Also get the calibrated RPOT values
    calibrated_rpot = np.loadtxt(f_name_calibrated_rpot, ndmin=2).astype(np.ushort)
    print(calibrated_rpot.dtype)

    # The phase will be varied in the following interval
    min_phase = min_phase_calibration
    max_phase = max_phase_calibration
    phase_step = phase_calibration_step

    phases = np.linspace(min_phase, max_phase,
                         int(np.rint((np.abs(min_phase) + np.abs(max_phase)) / phase_step) + 1))

    # Disable all speaker elements
    disable_all_speaker_elements_software()
    time.sleep(2)

    for f, freq in enumerate(l_frequencies):
        # For now, we target only one single frequency
        if int(freq) == 25000:
            print("Phase cal. frequency: " + str(freq))

            # We enable one speaker element as reference speaker
            # This will be speaker 0
            enable_specific_speaker_element(l_devices[0])
            change_speaker_settings(l_devices[0], freq, 0, calibrated_rpot[0, f])
            time.sleep(sleep_time_after_speaker_change)

            # Now we enable the other speakers one by one and sweep the phase
            for d, dev in enumerate(l_devices):
                if d != 0:
                    rms_tmp = np.zeros(len(phases))

                    # Ask if speaker is connected
                    print("Sweep device: " + str(d))
                    print("Press enter to continue")
                    while not keyboard.is_pressed('enter'):
                        pass

                    # Enable second speaker element
                    enable_specific_speaker_element(l_devices[d])
                    time.sleep(1)
                    change_speaker_settings(l_devices[d], freq, 0, calibrated_rpot[d, f])
                    time.sleep(sleep_time_after_speaker_change)

                    for p, phase_dif in enumerate(phases):
                        print("Phase shift: " + str(phase_dif))

                        # Phase shifts must be positive for STM32 code
                        if phase_dif < 0:
                            phase_dif = 360 - np.abs(phase_dif)

                        # Now we change the phase of the non-reference speaker element
                        change_speaker_settings(l_devices[d], freq, int(phase_dif), calibrated_rpot[d, f])
                        print("Phase: " + str(int(phase_dif)))
                        time.sleep(sleep_time_after_speaker_change)

                        # We calculated the microphone response
                        params = calculate_microphone_params(True)
                        rms_tmp[p] = params[0]

                    # Plot the response curve after phase shift calibration for a specific speaker
                    plt.clf()
                    plt.plot(rms_tmp)
                    plt.show()

                    # Save rms_tmp file for each speaker
                    f_tmp = "rms_tmp_phase_cal_speaker_" + str(d) + "_" + str(version) + ".txt"
                    np.savetxt(f_tmp, rms_tmp)

                    # Now we disable the non-reference speaker element
                    disable_specific_speaker_element(l_devices[d])
                    time.sleep(1)

    # Now we make sure to disable all speaker elements
    disable_all_speaker_elements_software()
    time.sleep(1)


def fit_func(x, a, b, c):
    return a + 2 * b * np.cos(np.deg2rad(x / 2)) * np.sin(c + np.deg2rad(x / 2))


def calculate_phase_offsets():
    global f_name_calibrated_speaker_sweep_info
    global min_phase_calibration
    global max_phase_calibration
    global phase_calibration_step
    global version
    global f_name_calibrated_phase_shifts_info
    global f_name_calibrated_phase_shifts

    # Speaker 0 is used as reference speaker
    # The other speakers are enabled one by one separately and the phase is shifted between [0° and 360°]
    # The resulting response should be a sine wave, and the phase offset is calculated through fitting

    # First, we read the info data from the amplitude calibration measurements
    f_info = open(f_name_calibrated_speaker_sweep_info, "r")
    str_devices = f_info.readline().rstrip('\n').lstrip("devices: ").replace(" ", "")
    l_devices = np.array(str_devices.split(",")).astype(np.ushort)
    print(l_devices)
    str_frequencies = f_info.readline().rstrip('\n').lstrip("frequencies: ").replace(" ", "")
    l_frequencies = np.array(str_frequencies.split(",")).astype(np.ushort)
    print(l_frequencies)
    f_info.close()

    # The phase was varied in the following interval
    min_phase_fitting = min_phase_calibration
    max_phase_fitting = max_phase_calibration
    phase_step_fitting = phase_calibration_step

    min_phase_plot = min_phase_calibration
    max_phase_plot = max_phase_calibration
    phase_step_plot = 1

    # Setting fitting arrays
    phases = np.linspace(min_phase_fitting, max_phase_fitting,
                         int(np.rint((np.abs(min_phase_fitting) + np.abs(max_phase_fitting)) / phase_step_fitting) + 1))
    phases_plot = np.linspace(min_phase_plot, max_phase_plot,
                              int(np.rint((np.abs(min_phase_plot) + np.abs(max_phase_plot)) / phase_step_plot) + 1))

    # Data buffer for the calculated phase shifts
    phase_shifts = np.zeros(len(l_devices))

    # Now we calculate the phase shifts through fitting
    for d, device in enumerate(l_devices):
        if d != 0:
            # Speaker 0 is used as reference speaker
            # We open the file with the corresponding phase measurement data based on the speaker IDs
            f_name_phase_data = "rms_tmp_phase_cal_speaker_" + str(d) + "_" + str(version) + ".txt"
            rms_phase_data = np.loadtxt(f_name_phase_data)

            # We apply fitting to calculate the phase offset
            popt, pcov = curve_fit(fit_func, phases, np.ravel(rms_phase_data))
            fitted_func = fit_func(phases, *popt)
            fitted_func_plot = fit_func(phases_plot, *popt)

            idx_max_rms_fitted = np.argmax(fitted_func_plot)
            angle_max_rms_fitted = phases_plot[idx_max_rms_fitted]
            print("Angle of max RMS fitted: " + str(angle_max_rms_fitted))

            # Plot measurement data and fitted curve to verify results
            plt.clf()
            plt.plot(rms_phase_data)
            plt.plot(fitted_func)
            plt.title("Fitted phase plot for speaker ID: " + str(d))
            plt.show()

            # Save phase offsets obtained through fitting
            phase_shifts[d] = angle_max_rms_fitted

    print(l_devices)
    print(devices)

    # Save phase offsets obtained through fitting
    np.savetxt(f_name_calibrated_phase_shifts, phase_shifts)
    file = open(f_name_calibrated_phase_shifts_info, "w")
    file.write("devices: " + str(devices).strip('[]') + '\n')
    file.write("frequencies: " + str(frequencies).strip('[]') + '\n')
    file.close()


def measure_frequency_response():
    global devices
    global frequencies
    global f_name_uncalibrated_speaker_sweep_info
    global f_name_uncalibrated_speaker_sweep
    global f_name_uncalibrated_speaker_sweep_min
    global f_name_uncalibrated_speaker_sweep_max
    global f_name_uncalibrated_speaker_sweep_std
    global default_rpot
    global sleep_time_after_speaker_change

    # Disable all speakers in the array
    disable_all_speaker_elements_software()
    time.sleep(2)

    # Data buffer
    rms_vs_freq = np.zeros((len(devices), len(frequencies)))
    min_rms_vs_freq = np.zeros((len(devices), len(frequencies)))
    max_rms_vs_freq = np.zeros((len(devices), len(frequencies)))
    std_rms_vs_freq = np.zeros((len(devices), len(frequencies)))

    # Connect each speaker separately
    for d, dev in enumerate(devices):

        # Ask if speaker is connected
        print("Sweep device: " + str(d))
        print("Press enter to continue")
        # enter = input("Press enter if connected")
        # while enter != "":
        #     pass
        while not keyboard.is_pressed('enter'):
            pass

        # Now that the speaker is connected, we can enable it
        enable_specific_speaker_element(dev)

        # Measure the speaker the speaker response
        for f, freq in enumerate(frequencies):
            print("Frequency: " + str(freq))

            # Change speaker settings
            change_speaker_settings(dev, freq, 0, default_rpot)
            time.sleep(sleep_time_after_speaker_change)

            # Calculate and get microphone parameters
            params = calculate_microphone_params(True)
            rms_vs_freq[d, f] = params[0]
            min_rms_vs_freq[d, f] = params[1]
            max_rms_vs_freq[d, f] = params[2]
            std_rms_vs_freq[d, f] = params[3]

        # Disable speaker and go to next one
        disable_specific_speaker_element(dev)
        time.sleep(1)

    # Save data in txt files
    np.savetxt(f_name_uncalibrated_speaker_sweep, rms_vs_freq)
    np.savetxt(f_name_uncalibrated_speaker_sweep_min, min_rms_vs_freq)
    np.savetxt(f_name_uncalibrated_speaker_sweep_max, max_rms_vs_freq)
    np.savetxt(f_name_uncalibrated_speaker_sweep_std, std_rms_vs_freq)

    # Write information file
    file = open(f_name_uncalibrated_speaker_sweep_info, "w")
    file.write("devices: " + str(devices).strip('[]') + '\n')
    file.write("frequencies: " + str(frequencies).strip('[]') + '\n')
    file.close()


def measure_calibrated_frequency_response():
    global devices
    global frequencies
    global f_name_calibrated_speaker_sweep_info
    global f_name_calibrated_speaker_sweep
    global f_name_calibrated_speaker_sweep_min
    global f_name_calibrated_speaker_sweep_max
    global f_name_calibrated_speaker_sweep_std
    global f_name_calibrated_rpot
    global sleep_time_after_speaker_change

    # Disable all speakers in the array
    disable_all_speaker_elements_software()
    time.sleep(2)

    # Open data files
    f_info = open(f_name_uncalibrated_speaker_sweep_info, "r")
    str_devices = f_info.readline().rstrip('\n').lstrip("devices: ").replace(" ", "")
    l_devices = np.array(str_devices.split(",")).astype(np.ushort)
    print(l_devices)
    str_frequencies = f_info.readline().rstrip('\n').lstrip("frequencies: ").replace(" ", "")
    l_frequencies = np.array(str_frequencies.split(",")).astype(np.ushort)
    print(l_frequencies)
    f_info.close()

    # Get calibrated rpot values
    calibrated_rpot = np.loadtxt(f_name_calibrated_rpot, ndmin=2).astype(np.ushort)
    print(calibrated_rpot.dtype)

    # Data buffer
    rms_vs_freq = np.zeros((len(devices), len(frequencies)))
    min_rms_vs_freq = np.zeros((len(devices), len(frequencies)))
    max_rms_vs_freq = np.zeros((len(devices), len(frequencies)))
    std_rms_vs_freq = np.zeros((len(devices), len(frequencies)))

    # Connect each speaker separately
    for d, dev in enumerate(devices):

        # Ask if speaker is connected
        print("Sweep device: " + str(d))
        print("Press enter to continue")
        # enter = input("Press enter if connected")
        # while enter != "":
        #     pass
        while not keyboard.is_pressed('enter'):
            pass

        # Now that the speaker is connected, we can enable it
        enable_specific_speaker_element(dev)

        # Measure the speaker response
        for f, freq in enumerate(frequencies):
            print("Frequency: " + str(freq))
            print("Calibrated RPOT: " + str(calibrated_rpot[d, f]))

            # Change speaker settings
            change_speaker_settings(dev, freq, 0, calibrated_rpot[d, f])
            time.sleep(sleep_time_after_speaker_change)

            # Calculate and get microphone parameters
            params = calculate_microphone_params(True)
            rms_vs_freq[d, f] = params[0]
            min_rms_vs_freq[d, f] = params[1]
            max_rms_vs_freq[d, f] = params[2]
            std_rms_vs_freq[d, f] = params[3]

        # Disable speaker and go to next one
        disable_specific_speaker_element(dev)
        time.sleep(1)

    # Save data in txt files
    np.savetxt(f_name_calibrated_speaker_sweep, rms_vs_freq)
    np.savetxt(f_name_calibrated_speaker_sweep_min, min_rms_vs_freq)
    np.savetxt(f_name_calibrated_speaker_sweep_max, max_rms_vs_freq)
    np.savetxt(f_name_calibrated_speaker_sweep_std, std_rms_vs_freq)

    # Write information file
    file = open(f_name_calibrated_speaker_sweep_info, "w")
    file.write("devices: " + str(devices).strip('[]') + '\n')
    file.write("frequencies: " + str(frequencies).strip('[]') + '\n')
    file.close()


def calibrate_speaker_responses():
    global f_name_uncalibrated_speaker_sweep_info
    global f_name_uncalibrated_speaker_sweep
    global f_name_error_file_response_calibration
    global default_rpot
    global f_name_calibrated_rpot

    # First, retrieve information from the uncalibrated frequency response measurement
    # Device information
    f_info = open(f_name_uncalibrated_speaker_sweep_info, "r")
    str_devices = f_info.readline().rstrip('\n').lstrip("devices: ").replace(" ", "")
    l_devices = str_devices.split(",")
    print(l_devices)

    # Frequency information
    str_frequencies = f_info.readline().rstrip('\n').lstrip("frequencies: ").replace(" ", "")
    l_frequencies = str_frequencies.split(",")
    print(l_frequencies)
    f_info.close()

    # If we get errors during amplitude calibration, we'll save this information in the following error file
    f = open(f_name_error_file_response_calibration, 'w')
    f.write("This is the error file\n")
    f.close()

    # Read uncalibrated frequency response data
    data = np.loadtxt(f_name_uncalibrated_speaker_sweep, ndmin=2)

    # Data buffer for calibrated RPOT values
    rpot = np.zeros((len(l_devices), len(l_frequencies)))
    target_resp_vs_freq = np.zeros(len(l_frequencies))

    # First, determine which speaker has the lowest response at a certain frequency
    for f, freq in enumerate(l_frequencies):
        dev_resp_at_freq = data[:, f]

        # Search speaker with lowest response at frequency freq: save ID and response value
        dev_min_resp = np.argmin(dev_resp_at_freq)
        min_resp = dev_resp_at_freq[dev_min_resp]

        # Indicate in RPOT data buffer which device has the lowest response: rpot value = default_rpot
        # If rpot value is zero, than this speaker has to be calibrated towards the lowest response
        for d, device in enumerate(l_devices):
            if d == dev_min_resp:
                rpot[d, f] = default_rpot
            else:
                rpot[d, f] = 0

        # Speaker with lowest response is saved in the 'target_resp_vs_freq' data buffer
        # We'll convert the measured response into dB
        target_resp_vs_freq[f] = min_resp
        print(target_resp_vs_freq)
        target_resp_vs_freq[f] = 20 * np.log10(target_resp_vs_freq[f])

    # Make sure all speakers are disabled before we start with the response calibration measurement
    disable_all_speaker_elements_software()

    # Now we know which speakers have the lowest response at each frequency
    # Hence we can calibrate to the lowest (target) responses
    for d, dev in enumerate(l_devices):
        # Ask if speaker is connected
        print("Sweep device: " + str(d))
        print("Press enter to continue")
        # enter = input("Press enter if connected")
        # while enter != "":
        #     pass
        while not keyboard.is_pressed('enter'):
            pass

        for f, freq in enumerate(l_frequencies):
            if rpot[d, f] != default_rpot:
                rpot[d, f] = calculate_rpot_target_resp(int(dev), d, int(freq), target_resp_vs_freq[f])
            else:
                pass  # Do nothing, because this speaker has the lowest response at this frequency

        # Save calibrated RPOT values
        np.savetxt(f_name_calibrated_rpot, rpot)


def calculate_rpot_target_resp(dev, d, freq, target_rms_db):
    global default_rpot
    global f_name_error_file_response_calibration
    global sleep_time_after_speaker_change

    print("Calibrate resp of speaker: " + str(d) + ", at frequency: " + str(freq))
    print("Target RMS: " + str(target_rms_db))

    # Start RPOT
    rpot = default_rpot

    # Enable speaker and change settings to frequency freq and default rpot
    enable_specific_speaker_element(dev)
    change_speaker_settings(dev, freq, 0, rpot)
    time.sleep(1)

    # Calculate measured microphone parameters
    params = calculate_microphone_params(False)
    rms_db = 20 * np.log10(params[0])
    print("RMS (dB): " + str(rms_db))

    # Check whether the measured speaker response is within the target response range
    have_same_resp = False

    if rms_db > target_rms_db + db_rms_deviation:
        have_same_resp = False
        rpot = rpot - 1000
    elif rms_db < target_rms_db - db_rms_deviation:
        print("WARNING: resp < target_resp!")
    else:
        have_same_resp = True
        print("Already within range!\n")

    # If the responses are still not the same, we'll have to calibrate the rpot values until both resp == target resp
    attempt_counter = 0

    while not have_same_resp:
        # Increase attempt counter
        attempt_counter = attempt_counter + 1

        # Change speaker settings with new rpot value
        change_speaker_settings(dev, freq, 0, rpot)
        time.sleep(sleep_time_after_speaker_change)

        # Calculate measured microphone parameters
        params = calculate_microphone_params(False)
        rms_db = 20 * np.log10(params[0])
        print("RMS (dB): " + str(rms_db) + " at RPOT: " + str(rpot))

        if rms_db < target_rms_db - db_rms_deviation:
            have_same_resp = False
            rpot = rpot + 150
        elif rms_db > target_rms_db + db_rms_deviation:
            have_same_resp = False


            rpot = round(rpot - 500)
        else:
            have_same_resp = True
            print("Now response in range!")

        if attempt_counter >= 30 or rpot - 1000 < 0:
            have_same_resp = True
            last_rpot_tested = rpot
            rpot = 0

            print("Check error file!")
            f_error = open(f_name_error_file_response_calibration, 'a')
            f_error.write("Error for device: " + str(d) + " at frequency: " + str(freq) + "\n")
            f_error.write("Target RMS dB: " + str(target_rms_db) + ", RMS dB: " + str(rms_db) + "\n")
            f_error.write("RPOT: " + str(last_rpot_tested) + "\n")
            f_error.close()

    # Disable speaker
    disable_specific_speaker_element(dev)
    time.sleep(1)

    # Return calibrated RPOT value that produces same response as target response (= speaker with lowest response)
    return rpot


def calculate_beam_steering_phase_shifts(angle):
    # Theoretical phase shifts to steer beam towards angle
    signal_phase_beam_steering = np.round(180 * np.sin(np.deg2rad(angle)), 0)
    return signal_phase_beam_steering


def set_speakers(setCalibrated):
    global f_name_calibrated_rpot
    global f_name_calibrated_phase_shifts
    global f_name_calibrated_phase_shifts_info
    global steering_angle
    global devices

    if setCalibrated:
        f_info = open(f_name_calibrated_phase_shifts_info, "r")
        str_devices = f_info.readline().rstrip('\n').lstrip("devices: ").replace(" ", "")
        l_devices = np.array(str_devices.split(",")).astype(np.ushort)
        print(l_devices)
        str_frequencies = f_info.readline().rstrip('\n').lstrip("frequencies: ").replace(" ", "")
        l_frequencies = np.array(str_frequencies.split(",")).astype(np.ushort)
        print(l_frequencies)
        f_info.close()

        calibrated_rpot = np.loadtxt(f_name_calibrated_rpot, ndmin=2).astype(np.ushort)
        calibrated_phase_shifts = np.loadtxt(f_name_calibrated_phase_shifts, ndmin=2)

        # Print calibrated phase shifts
        print("Calibrated phase shifts:")
        print(calibrated_phase_shifts)

        # Calculate signal offset for beam steering and add them to the calibrated signal phase offsets
        phase_offset_beam_steering = calculate_beam_steering_phase_shifts(steering_angle)
        print("Beam steering offset: " + str(phase_offset_beam_steering))
        beam_steering_phase_shifts = np.zeros(len(calibrated_phase_shifts))
        for d, dev in enumerate(l_devices):
            beam_steering_phase_shifts[d] = calibrated_phase_shifts[d] + d * phase_offset_beam_steering

        print("Non adjusted beam steering phase shifts: ")
        print(beam_steering_phase_shifts)

        print("Adjusted beam steering phase shifts [-180, 180]: ")
        # Adjust phases to be in range [-180, 180]
        beam_steering_phase_shifts = (beam_steering_phase_shifts + 180) % 360 - 180
        print(beam_steering_phase_shifts)

        print("Adjusted beam steering phase shifts [>0]: ")
        beam_steering_phase_shifts[beam_steering_phase_shifts < 0] = beam_steering_phase_shifts[
                                                                         beam_steering_phase_shifts < 0] + 360
        print(beam_steering_phase_shifts)

        # save calibrated phase shifts
        calibrated_phase_shifts = beam_steering_phase_shifts

        idx_freq = str_frequencies.split(',').index("25000")
        freq = l_frequencies[idx_freq]
        print("Frequency set: " + str(freq))

        # Disable all speaker elements
        disable_all_speaker_elements_software()
        time.sleep(2)

        # Then enable them all, one by one
        for d, device in enumerate(devices):
            print("ON: " + str(d))
            enable_specific_speaker_element(l_devices[d])
            change_speaker_settings(l_devices[d], int(freq), int(calibrated_phase_shifts[d]),
                                    int(calibrated_rpot[d, idx_freq]))
            time.sleep(1)

    else:
        # Disable all speaker elements
        disable_all_speaker_elements_software()
        time.sleep(2)

        # Then enable them all, one by one
        for d, device in enumerate(devices):
            print("ON: " + str(d))
            enable_specific_speaker_element(devices[d])
            change_speaker_settings(devices[d], 25000, 0, 12000)
            time.sleep(1)


def measure_response_pattern_in_az_layers(inNumberOfSteps):
    global current_angle_az
    global turn_degree_az
    global f_name_beam_pattern_base
    global rms_vs_angle

    if inNumberOfSteps:
        pass
        # TODO
    else:
        try:
            # In this section, we will turn the stepper motor in number of angles
            # The arduino will convert the angle into the required number of steps

            current_angle = 0

            # First, we set the stepper at -180
            # In this way, we get a nice continuous beam pattern when we're passing 0°
            set_stepper_at_angle_relative_to_base_az(-180)
            current_angle_az = -180

            for i in range(0, total_turns_one_revolution_from_angle_az):
                # Calculate microphone params
                params = calculate_microphone_params(True)
                rms_vs_angle[0][i] = params[0]  # current elevation = 0

                # Display current beam pattern and microphone signal
                display_current_beam_pattern(True, params)

                # Set stepper to the next azimuth angle
                next_angle_az = round(current_angle_az + turn_degree_az)
                print("Set stepper to next az angle: " + str(next_angle_az))
                set_stepper_at_angle_relative_to_base_az(next_angle_az)
                current_angle_az = next_angle_az

            # At the end, set stepper back to 0°
            set_stepper_at_angle_relative_to_base_az(0)
            current_angle_az = 0

            # Save beam pattern data
            f_name_beam_pattern = f_name_beam_pattern_base + "_" + time.strftime("%Y%m%d-%H%M%S.txt")
            np.savetxt(f_name_beam_pattern, rms_vs_angle)
            write_measurement_info()

        except:
            set_stepper_at_angle_relative_to_base_az(0)


def display_current_beam_pattern(save_plot, microphone_params):
    global total_turns_one_revolution_from_angle_az
    global rms_vs_angle

    # Close current figure
    plt.close()

    # Display both beam pattern and microphone response (for evaluation during measurements)
    fig = plt.figure()
    ax1 = plt.subplot(121, projection='polar')
    ax2 = plt.subplot(122)

    theta = np.linspace(-np.pi, np.pi, total_turns_one_revolution_from_angle_az)
    ax1.plot(theta, rms_vs_angle[0, :])  # Current elevation angle = 0

    microphone_signal = microphone_params[4]
    ax2.plot(np.linspace(0, 100, 100), microphone_signal[0:100])

    # Update beam pattern
    plt.show()

    if save_plot:
        plt.title("Beam pattern (" + str(array_configuration) + ")")
        f_name = "Current_beam_pattern_" + str(array_configuration) + ".svg"
        fig.savefig(f_name, bbox_inches='tight')


def write_measurement_info():
    global f_name_beam_pattern_base

    global array_configuration
    global version
    global freq
    global dist
    global beam_angle
    global turn_degree_az

    # Save beam pattern data
    f_name_beam_pattern_info = f_name_beam_pattern_base + "_" + time.strftime("%Y%m%d-%H%M%S") + "_info.txt"

    file = open(f_name_beam_pattern_info, "a")

    file.write("array_config: " + array_configuration + '\n')
    file.write("frequency: " + freq + '\n')
    file.write("distance: " + dist + '\n')
    file.write("version: " + version + '\n')
    file.write("beam_angle: " + beam_angle + '\n')
    file.write("az_angle_step: " + str(turn_degree_az) + '\n')

    file.write("sample_rate: " + str(sample_rate) + '\n')
    file.write("num_samples: " + str(num_samples) + '\n')
    file.write("num_samples_loops: " + str(num_sample_loops) + '\n')
    file.write("date_time: " + str(time.strftime("%Y%m%d-%H%M%S.txt")) + '\n')

    file.close()


# MAIN

calibrate_amplitude()
calibrate_phase()

set_speakers(True)
start_arduino_serial()
measure_response_pattern_in_az_layers(False)

disable_all_speaker_elements_software()
