# Copyright 2018 Tensorforce Team. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================

from tensorforce.agents import PolicyAgent


class VanillaPolicyGradient(PolicyAgent):
    """
    [Vanilla Policy Gradient](https://link.springer.com/article/10.1007/BF00992696) agent
    (specification key: `vpg`).
    """

    def __init__(
        # Environment
        self, states, actions, max_episode_timesteps,
        # Network
        network='auto',
        # Optimization
        batch_size=10, update_frequency=None, learning_rate=3e-4,
        # Reward estimation
        discount=0.99, estimate_terminal=False,
        # Baseline
        baseline_network=None, baseline_optimizer=1.0,
        # Preprocessing
        preprocessing=None,
        # Exploration
        exploration=0.0, variable_noise=0.0,
        # Regularization
        l2_regularization=0.0, entropy_regularization=0.0,
        # TensorFlow etc
        name='agent', device=None, parallel_interactions=1, seed=None, execution=None, saver=None,
        summarizer=None, recorder=None, config=None
    ):
        memory = dict(type='recent', capacity=((batch_size + 1) * max_episode_timesteps))
        if update_frequency is None:
            update = dict(unit='episodes', batch_size=batch_size)
        else:
            update = dict(unit='episodes', batch_size=batch_size, frequency=update_frequency)
        optimizer = dict(type='adam', learning_rate=learning_rate)
        objective = 'policy_gradient'
        if baseline_network is None:
            reward_estimation = dict(horizon='episode', discount=discount)
            baseline_policy = None
            assert baseline_optimizer == 1.0
            baseline_optimizer = None
            baseline_objective = None
        else:
            reward_estimation = dict(
                horizon='episode', discount=discount,
                estimate_horizon=('late' if estimate_terminal else False),
                estimate_terminal=estimate_terminal, estimate_advantage=True
            )
            # State value doesn't exist for Beta
            baseline_policy = dict(network=baseline_network, distributions=dict(float='gaussian'))
            baseline_objective = 'state_value'

        super().__init__(
            # Agent
            states=states, actions=actions, max_episode_timesteps=max_episode_timesteps,
            parallel_interactions=parallel_interactions, buffer_observe=True, seed=seed,
            recorder=recorder, config=config,
            # Model
            name=name, device=device, execution=execution, saver=saver, summarizer=summarizer,
            preprocessing=preprocessing, exploration=exploration, variable_noise=variable_noise,
            l2_regularization=l2_regularization,
            # PolicyModel
            policy=None, network=network, memory=memory, update=update, optimizer=optimizer,
            objective=objective, reward_estimation=reward_estimation,
            baseline_policy=baseline_policy, baseline_network=None,
            baseline_optimizer=baseline_optimizer, baseline_objective=baseline_objective,
            entropy_regularization=entropy_regularization
        )
