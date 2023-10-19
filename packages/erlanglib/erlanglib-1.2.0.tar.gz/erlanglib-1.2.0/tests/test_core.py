import unittest

from erlanglib import factorial, calculate_erlangs, \
     erlang_b, required_channels, calculate_erlangs_from_blocking, \
     calls_per_second_from_erlangs,call_duration_from_erlangs, \
     erlang_c, service_level, average_speed_of_answer, \
     immediate_answer_percentage, occupancy, required_agents, \
     calculate_erlangs_seconds, calculate_erlangs_minutes


class TestErlangLib(unittest.TestCase):

    def test_factorial(self):

        # factorial 0 = 1 .... there are positive values <0
        self.assertEqual(factorial(0), 1)

        # factorial 1 = 1
        self.assertEqual(factorial(1), 1)

        # factorial 2 = 2
        self.assertEqual(factorial(2), 2)

        # factorial 3 = 6
        self.assertEqual(factorial(3), 6)

        # factorial 4 = 24
        self.assertEqual(factorial(4), 24)

        # self.assertEqual(factorial(708), 5)

    def test_calculate_erlangs(self):

        # Testing for half an hour call duration with 120 calls initiated per hour
        # Expected: 0.5 hours * 120 calls/hour = 60 Erlangs
        self.assertAlmostEqual(calculate_erlangs(0.5, 120), 60)

        # Testing for an hour call duration with 60 calls initiated per hour
        # Expected: 1 hour * 60 calls/hour = 60 Erlangs
        self.assertAlmostEqual(calculate_erlangs(1, 60), 60)

        # Testing for no call duration (0 hours) with 60 calls initiated per hour
        # Expected: 0 hours * 60 calls/hour = 0 Erlangs
        self.assertAlmostEqual(calculate_erlangs(0, 60), 0)

        # Testing for an hour call duration with no calls initiated (0 calls/hour)
        # Expected: 1 hour * 0 calls/hour = 0 Erlangs
        self.assertAlmostEqual(calculate_erlangs(1, 0), 0)

    def test_calculate_erlangs_seconds(self):

        # 1800 seconds is 0.5 hours, 1 call per second is 3600 calls per hour
        self.assertAlmostEqual(calculate_erlangs_seconds(1800, 1), 0.5 * 3600)

        # 3600 seconds is 1 hour, 0.5 calls per second is 1800 calls per hour
        self.assertAlmostEqual(calculate_erlangs_seconds(3600, 0.5), 1 * 1800)

    def test_calculate_erlangs_minutes(self):

        # 30 minutes is 0.5 hours, 2 calls per minute is 120 calls per hour
        self.assertAlmostEqual(calculate_erlangs_minutes(30, 2), 0.5 * 120)

        # 60 minutes is 1 hour, 1 call per minute is 60 calls per hour
        self.assertAlmostEqual(calculate_erlangs_minutes(60, 1), 1 * 60)

    def test_calls_per_second_from_erlangs(self):

        # Given Erlangs of 48,000 and a call duration of 8 minutes (480 seconds) = 100 calls per second
        self.assertAlmostEqual(calls_per_second_from_erlangs(48000, 480), 100, places=2)

    def test_call_duration_from_erlangs(self):

        # Given Erlangs of 48,000 and 100 calls per second = 480 seconds call duration
        self.assertAlmostEqual(call_duration_from_erlangs(48000, 100), 480, places=2)

    def test_erlang_b(self):

        # For 10 channels (N) and offered load (A) 5 Erlangs =  0.018384570336648136 = 1.8%
        self.assertAlmostEqual(erlang_b(10, 5), 0.018384, places=4)

        # For 10 channels (N) and offered load (A) 20 Erlangs =  0.5379631686320729 = 53.8%
        self.assertAlmostEqual(erlang_b(10, 20), 0.53796, places=4)

        # For 2510 channels (N) and offered load (A) 708 Erlangs =  0.0000 = 0.00%
        self.assertAlmostEqual(erlang_b(2510, 708), 0.0000, places=4)

    def test_required_channels(self):

        A = 5
        target_blocking = 0.010
        # For an offered load (A) 5 Erlangs and a targeted blocking probability (B) of 1% = 11 channels needed
        self.assertTrue(required_channels(A, target_blocking), 11)

        A = 10
        target_blocking = 0.010
        # For an offered load (A) 10 Erlangs and a targeted blocking probability (B) of 1% = 18 channels needed
        self.assertEqual(required_channels(A, target_blocking), 18)

        A = 708
        target_blocking = 0.01
        # For an offered load (A) 708 Erlangs and a targeted blocking probability (B) of 1% = 736 channels needed
        self.assertEqual(required_channels(A, target_blocking), 736)

    def test_calculate_erlangs_from_blocking(self):

        # For 10 channels and target blocking probability 0.0184 (1.84%) = 5
        self.assertAlmostEqual(calculate_erlangs_from_blocking(10, 0.0184), 5, places=1)

        # For 10 channels and target blocking probability 0.53796 (53.8%) = 20
        self.assertAlmostEqual(calculate_erlangs_from_blocking(10, 0.53796), 20, places=1)

        self.assertAlmostEqual(calculate_erlangs_from_blocking(2510,0.000001), 2144.77, places=1)

    def test_erlang_c(self):

        # For 12 servers (N) and offered load (A) 10 Erlangs the probability a call will wait = 0.2853 = 28.53 %
        self.assertAlmostEqual(erlang_c(11, 10), 0.6821, places=4)

        # For 14 servers (N) and offered load (A) 10 Erlangs the probability a call will wait = 0.2853 = 28.53 %
        self.assertAlmostEqual(erlang_c(14, 10), 0.1741, places=4)

    def test_service_level(self):

        N = 11  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        target_time_seconds = 20
        AHT_seconds = 180
        expected_service_level = 0.390
        self.assertAlmostEqual(service_level(N, A, Pw, target_time_seconds, AHT_seconds), expected_service_level,
                               places=2)

        N = 12  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        target_time_seconds = 20
        AHT_seconds = 180
        expected_service_level = 0.640
        self.assertAlmostEqual(service_level(N, A, Pw, target_time_seconds, AHT_seconds), expected_service_level,
                               places=2)

        N = 14  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        target_time_seconds = 20
        AHT_seconds = 180
        expected_service_level =  0.888350
        self.assertAlmostEqual(service_level(N, A, Pw, target_time_seconds, AHT_seconds), expected_service_level,
                               places=2)

    def test_average_speed_of_answer(self):

        N = 14  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)
        average_handling_time = 180

        expected_asa = 7.83593
        self.assertAlmostEqual(average_speed_of_answer(N, A, Pw, average_handling_time), expected_asa, places=2)

    def test_immediate_answer_percentage(self):

        N = 14  # Number of agents
        A = 10  # Traffic in Erlangs
        Pw = erlang_c(N, A)

        expected_percentage = 82.586
        self.assertAlmostEqual(immediate_answer_percentage(Pw), expected_percentage, places=2)

    def test_occupancy(self):

        A = 10  # Traffic in Erlangs
        N = 14  # Number of agents

        expected_occupancy = 71.4285
        self.assertAlmostEqual(occupancy(A, N), expected_occupancy, places=2)

    def test_required_agents(self):

        # For raw agents = 14 and shrinkage = 30%
        # required agents = 14 / (1 - 0.30) = 20 agents
        self.assertEqual(required_agents(14, 30), 20)

        # For raw agents = 50 and shrinkage = 20%
        # required agents = 50 / (1 - 0.20) = 62.5 which rounds to 63
        self.assertEqual(required_agents(50, 20), 63)


if __name__ == '__main__':
    unittest.main()
