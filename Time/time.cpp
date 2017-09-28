// ======================time.cpp =========================

#include <uhd/utils/thread_priority.hpp>
#include <uhd/utils/safe_main.hpp>
#include <uhd/usrp/multi_usrp.hpp>
#include <uhd/exception.hpp>
#include <uhd/types/tune_request.hpp>
#include <boost/program_options.hpp>
#include <boost/format.hpp>
#include <boost/thread.hpp>
#include <boost/signals2/mutex.hpp>
#include <boost/math/special_functions/round.hpp>
#include <boost/algorithm/string.hpp>
#include <boost/lexical_cast.hpp>
#include <boost/filesystem.hpp>
#include <Eigen/Dense>
#include <Eigen/SVD>
#include <vector>
#include <iostream>
#include <fstream>
#include <complex>
#include <csignal>
#include <stdint.h>
#include <cmath>

#define pi 3.14159265358979323846

using namespace Eigen;
using namespace std;
namespace po = boost::program_options;


static bool stop_signal_called = false;		// control signal of all threads
boost::mutex mtx;							// mutex for global variables below
VectorXcf global_tx, global_rx;				// long global buffers for the storage of TX/RX buffer
int global_num[2] = {0, 0};					// # of TX/RX buffer in global_tx, rx
int gsize;

void sig_int_handler (int) {stop_signal_called = true;}


int UHD_SAFE_MAIN(int argc, char *argv[])
{
	string cpu, wire, subdev, a1, a2, ref, pps, tx_args, rx_args, usrp_args;
	cpu = "fc32";
	wire = "sc16";
	subdev = "A:A";
	a1 = "TX/RX";
	a2 = "RX2";
	ref = "internal";
	pps = "internal";
	string file[3] = {"tx_file", "rx_file", "y_clean_file"};

	double freq, gain, total_num_samps, total_time, bw;		// default setting 
	freq = 915e6;
	gain = 65;
	bw = 1e6;
	total_num_samps = 0;
	total_time = 20;

	double rate, tx_gain, rx_gain;		// parameters set by po
	float ampl;

	double wave_freq_1, wave_space;								// about multi-sine generation
	int wave_num;										// 4 tones by default
	
	VectorXf w_freq(8);									// for all frequency: should be different from wave_freq

	uhd::set_thread_priority();

	po::options_description desc("Allowed options");
	desc.add_options()
		("tx_args",po::value<string>(&tx_args)->default_value(""),"uhd device address args")
		("rx_args",po::value<string>(&rx_args)->default_value(""),"uhd device address args")
		("rate", po::value<double>(&rate)->default_value(2e6), "rate of transmit and receive samples")
        	("ampl", po::value<float>(&ampl)->default_value(float(0.3)), "amplitude of the waveform [0 to 0.7]")
		("tx-gain", po::value<double>(&tx_gain)->default_value(gain), "gain for the transmit RF chain")
		("rx-gain", po::value<double>(&rx_gain)->default_value(gain), "gain for the receive RF chain")
		("wave-num", po::value<int>(&wave_num)->default_value(4), "number of sine wave tones")
		("wave-freq-1", po::value<double>(&wave_freq_1)->default_value(100e3), "1st waveform frequency in Hz")
		("wave-space", po::value<double>(&wave_space)->default_value(100e3), "spacing between adjacent tones")
		("freq-1", po::value<float>(&w_freq(0))->default_value(0), "1st tone of sine wave")
		("freq-2", po::value<float>(&w_freq(1))->default_value(0), "2nd tone of sine wave")
		("freq-3", po::value<float>(&w_freq(2))->default_value(0), "3rd tone of sine wave")
		("freq-4", po::value<float>(&w_freq(3))->default_value(0), "4th tone of sine wave")
		("freq-5", po::value<float>(&w_freq(4))->default_value(0), "5th tone of sine wave")
		("freq-6", po::value<float>(&w_freq(5))->default_value(0), "6th tone of sine wave")
		("freq-7", po::value<float>(&w_freq(6))->default_value(0), "7th tone of sine wave")
		("freq-8", po::value<float>(&w_freq(7))->default_value(0), "8th tone of sine wave")
		;
	po::variables_map vm;
	po::store(po::parse_command_line(argc, argv, desc), vm);
	po::notify(vm);


	// set the usrp
	uhd::usrp::multi_usrp::sptr tx_usrp = uhd::usrp::multi_usrp::make(tx_args);
	uhd::usrp::multi_usrp::sptr rx_usrp = uhd::usrp::multi_usrp::make(rx_args);
	uhd::usrp::multi_usrp::sptr usrp = uhd::usrp::multi_usrp::make(usrp_args);

	tx_usrp->set_clock_source(ref);
	tx_usrp->set_tx_rate(rate);
	rx_usrp->set_rx_rate(rate);
	cout<<boost::format("Actual tx rate: %f Msps ...")%(tx_usrp->get_tx_rate()/1e6)<<endl;
	cout<<boost::format("Actual rx rate: %f Msps ...")%(rx_usrp->get_rx_rate()/1e6)<<endl;

	tx_usrp->set_tx_antenna(a1);
	rx_usrp->set_rx_antenna(a2);
	
	tx_usrp->set_tx_bandwidth(bw);
	rx_usrp->set_rx_bandwidth(bw);

	tx_usrp->set_tx_freq(freq);
	rx_usrp->set_rx_freq(freq);

	tx_usrp->set_tx_gain(tx_gain);
	rx_usrp->set_rx_gain(rx_gain);
	
	tx_usrp->set_tx_subdev_spec(subdev);
	rx_usrp->set_rx_subdev_spec(subdev);

	std::cout<<boost::format("Using TX Device: %s") % tx_usrp->get_pp_string()<<endl;
	std::cout<<boost::format("Using RX Device: %s") % rx_usrp->get_pp_string()<<endl;
    

	// // set transmit & receive streamer
	// uhd::stream_args_t stream_args(cpu, wire);
	// uhd::tx_streamer::sptr tx = tx_usrp->get_tx_stream(stream_args);
	// uhd::rx_streamer::sptr rx = rx_usrp->get_rx_stream(stream_args);
	// int spb = tx->get_max_num_samps() * 10;
	// tx_usrp->set_time_now(0.0);
	


	// // check rdf and L0 lock detect is here
 //    std::vector<std::string> tx_sensor_names, rx_sensor_names;
 //    tx_sensor_names = tx_usrp->get_tx_sensor_names(0);
 //    if (std::find(tx_sensor_names.begin(), tx_sensor_names.end(), "lo_locked") != tx_sensor_names.end()) {
 //        uhd::sensor_value_t lo_locked = tx_usrp->get_tx_sensor("lo_locked",0);
 //        std::cout << boost::format("Checking TX: %s ...") % lo_locked.to_pp_string() << std::endl;
 //        UHD_ASSERT_THROW(lo_locked.to_bool());
 //    }
 //    rx_sensor_names = rx_usrp->get_rx_sensor_names(0);
 //    if (std::find(rx_sensor_names.begin(), rx_sensor_names.end(), "lo_locked") != rx_sensor_names.end()) {
 //        uhd::sensor_value_t lo_locked = rx_usrp->get_rx_sensor("lo_locked",0);
 //        std::cout << boost::format("Checking RX: %s ...") % lo_locked.to_pp_string() << std::endl;
 //        UHD_ASSERT_THROW(lo_locked.to_bool());
 //    }
 //    tx_sensor_names = tx_usrp->get_mboard_sensor_names(0);

	// if (total_num_samps == 0){
	// 	std::signal(SIGINT, &sig_int_handler);
	// 	std::cout << "Press Ctrl + C to stop streaming..." << std::endl;
	// }

	
    //reset usrp time to prepare for transmit/receive
	double t=0;
	int i=0;

    t = usrp->get_time_now().get_real_secs();
	std::cout << boost::format("Current time is: ") << t <<std::endl;

	std::cout << boost::format("Setting device timestamp to 0...") << std::endl;
    tx_usrp->set_time_now(uhd::time_spec_t(0.0));
	
	for(i=0; i<10; i++){
    t = usrp->get_time_now().get_real_secs();
	std::cout << boost::format("Current time is: ") << t <<std::endl;
	}
	// // set up metadata for transmitter
	// uhd::tx_metadata_t md;
	// md.start_of_burst = true;				// set start of burst to true for 1st packet in the chain
	// md.end_of_burst = false;                // set end of burst to true for the last packet in the chain
	// md.has_time_spec = true;                // set true to send at the time specified by time spec; set false to send immediately
	// md.time_spec = uhd::time_spec_t(0.1);
	

	// // set up signal structure and generate preamble from multi-tone frequency
	// int start = 30;
	// int preamble_length = rate/wave_freq_1;
	// int estimator_length = 42;
	// int pilot_length = 600;
	// int signal_length = spb;
	// int len[4] = {estimator_length, preamble_length, pilot_length, signal_length};
	// VectorXf preamble = mt_sine.segment(0, preamble_length).real();

	


	//finished
	stop_signal_called = true;	
	cout<<"-- Done!"<<endl<<endl;
	return EXIT_SUCCESS;

}
