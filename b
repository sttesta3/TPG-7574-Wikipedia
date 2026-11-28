Attaching to agregador_top_0, agregador_top_1, agregador_top_2, clasificador_0, clasificador_1, clasificador_2, cliente_0, cuenta_prom_0, cuenta_prom_1, cuenta_prom_2, gateway, img_descargador_0, img_descargador_1, join_top_0, join_top_1, join_top_2, maestro_0, maestro_1, maestro_2, promedio_0, promedio_1, promedio_2, rabbitmq, sum_top_0, sum_top_1, sum_top_2, nodo-base-1, transformador_0, transformador_1, transformador_2
[Knodo-base-1 exited with code 0
rabbitmq     | 2026-11-27 23:59:17.605259+00:00 [info] <0.228.0> Feature flags: list of feature flags found:
rabbitmq     | 2026-11-27 23:59:17.615046+00:00 [info] <0.228.0> Feature flags:   [ ] implicit_default_bindings
rabbitmq     | 2026-11-27 23:59:17.615093+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status
rabbitmq     | 2026-11-27 23:59:17.615111+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue
rabbitmq     | 2026-11-27 23:59:17.615132+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue
rabbitmq     | 2026-11-27 23:59:17.615190+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits
rabbitmq     | 2026-11-27 23:59:17.615210+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata
rabbitmq     | 2026-11-27 23:59:17.615226+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes
rabbitmq     | 2026-11-27 23:59:17.911723+00:00 [noti] <0.44.0> Application syslog exited with reason: stopped
rabbitmq     | 2026-11-27 23:59:17.911824+00:00 [noti] <0.228.0> Logging: switching to configured handler(s); following messages may not be visible in this log output
rabbitmq     | [38;5;87m2026-11-27 23:59:17.922365+00:00 [notice] <0.228.0> Logging: configured log handlers are now ACTIVE[0m
rabbitmq     | 2026-11-27 23:59:18.058294+00:00 [info] <0.228.0> ra: starting system quorum_queues[0m
rabbitmq     | 2026-11-27 23:59:18.058363+00:00 [info] <0.228.0> starting Ra system: quorum_queues in directory: /var/lib/rabbitmq/mnesia/rabbit@dc96961bdc36/quorum/rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:18.101788+00:00 [info] <0.264.0> ra system 'quorum_queues' running pre init for 0 registered servers[0m
rabbitmq     | 2026-11-27 23:59:18.107396+00:00 [info] <0.265.0> ra: meta data store initialised for system quorum_queues. 0 record(s) recovered[0m
rabbitmq     | [38;5;87m2026-11-27 23:59:18.116166+00:00 [notice] <0.270.0> WAL: ra_log_wal init, open tbls: ra_log_open_mem_tables, closed tbls: ra_log_closed_mem_tables[0m
rabbitmq     | 2026-11-27 23:59:18.120069+00:00 [info] <0.228.0> ra: starting system coordination[0m
rabbitmq     | 2026-11-27 23:59:18.120128+00:00 [info] <0.228.0> starting Ra system: coordination in directory: /var/lib/rabbitmq/mnesia/rabbit@dc96961bdc36/coordination/rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:18.120836+00:00 [info] <0.277.0> ra system 'coordination' running pre init for 0 registered servers[0m
rabbitmq     | 2026-11-27 23:59:18.121218+00:00 [info] <0.278.0> ra: meta data store initialised for system coordination. 0 record(s) recovered[0m
rabbitmq     | [38;5;87m2026-11-27 23:59:18.121345+00:00 [notice] <0.283.0> WAL: ra_coordination_log_wal init, open tbls: ra_coordination_log_open_mem_tables, closed tbls: ra_coordination_log_closed_mem_tables[0m
rabbitmq     | 2026-11-27 23:59:18.123213+00:00 [info] <0.228.0> [0m
rabbitmq     | 2026-11-27 23:59:18.123213+00:00 [info] <0.228.0>  Starting RabbitMQ 3.9.16 on Erlang 24.3.4 [jit][0m
rabbitmq     | 2026-11-27 23:59:18.123213+00:00 [info] <0.228.0>  Copyright (c) 2007-2022 VMware, Inc. or its affiliates.[0m
rabbitmq     | 2026-11-27 23:59:18.123213+00:00 [info] <0.228.0>  Licensed under the MPL 2.0. Website: https://rabbitmq.com[0m
rabbitmq     | 
rabbitmq     |   ##  ##      RabbitMQ 3.9.16
rabbitmq     |   ##  ##
rabbitmq     |   ##########  Copyright (c) 2007-2022 VMware, Inc. or its affiliates.
rabbitmq     |   ######  ##
rabbitmq     |   ##########  Licensed under the MPL 2.0. Website: https://rabbitmq.com
rabbitmq     | 
rabbitmq     |   Erlang:      24.3.4 [jit]
rabbitmq     |   TLS Library: OpenSSL - OpenSSL 1.1.1o  3 May 2022
rabbitmq     | 
rabbitmq     |   Doc guides:  https://rabbitmq.com/documentation.html
rabbitmq     |   Support:     https://rabbitmq.com/contact.html
rabbitmq     |   Tutorials:   https://rabbitmq.com/getstarted.html
rabbitmq     |   Monitoring:  https://rabbitmq.com/monitoring.html
rabbitmq     | 
rabbitmq     |   Logs: /var/log/rabbitmq/rabbit@dc96961bdc36_upgrade.log
rabbitmq     |         <stdout>
rabbitmq     | 
rabbitmq     |   Config file(s): /etc/rabbitmq/conf.d/10-defaults.conf
rabbitmq     | 
rabbitmq     |   Starting broker...2026-11-27 23:59:18.123907+00:00 [info] <0.228.0> [0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>  node           : rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>  home dir       : /var/lib/rabbitmq[0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>  config file(s) : /etc/rabbitmq/conf.d/10-defaults.conf[0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>  cookie hash    : i3JQ5Ef6Fr6YXRyZm8jimw==[0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>  log(s)         : /var/log/rabbitmq/rabbit@dc96961bdc36_upgrade.log[0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>                 : <stdout>[0m
rabbitmq     | 2026-11-27 23:59:18.123907+00:00 [info] <0.228.0>  database dir   : /var/lib/rabbitmq/mnesia/rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:18.298734+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:18.298788+00:00 [info] <0.228.0> Feature flags:   [ ] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:18.298810+00:00 [info] <0.228.0> Feature flags:   [ ] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:18.298840+00:00 [info] <0.228.0> Feature flags:   [ ] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:18.298884+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:18.298902+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:18.298918+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:18.298970+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:18.298988+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:18.299005+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.277546+00:00 [info] <0.228.0> Running boot step pre_boot defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.277626+00:00 [info] <0.228.0> Running boot step rabbit_global_counters defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.277845+00:00 [info] <0.228.0> Running boot step rabbit_osiris_metrics defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.277988+00:00 [info] <0.228.0> Running boot step rabbit_core_metrics defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.278682+00:00 [info] <0.228.0> Running boot step rabbit_alarm defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.280891+00:00 [info] <0.295.0> Memory high watermark set to 6374 MiB (6684552396 bytes) of 15937 MiB (16711380992 bytes) total[0m
rabbitmq     | 2026-11-27 23:59:20.283002+00:00 [info] <0.297.0> Enabling free disk space monitoring[0m
rabbitmq     | 2026-11-27 23:59:20.283047+00:00 [info] <0.297.0> Disk free limit set to 50MB[0m
rabbitmq     | 2026-11-27 23:59:20.285111+00:00 [info] <0.228.0> Running boot step code_server_cache defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.285192+00:00 [info] <0.228.0> Running boot step file_handle_cache defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.285366+00:00 [info] <0.302.0> Limiting to approx 1048479 file handles (943629 sockets)[0m
rabbitmq     | 2026-11-27 23:59:20.285472+00:00 [info] <0.303.0> FHC read buffering: OFF[0m
rabbitmq     | 2026-11-27 23:59:20.285509+00:00 [info] <0.303.0> FHC write buffering: ON[0m
rabbitmq     | 2026-11-27 23:59:20.285753+00:00 [info] <0.228.0> Running boot step worker_pool defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.285800+00:00 [info] <0.285.0> Will use 12 processes for default worker pool[0m
rabbitmq     | 2026-11-27 23:59:20.285835+00:00 [info] <0.285.0> Starting worker pool 'worker_pool' with 12 processes in it[0m
rabbitmq     | 2026-11-27 23:59:20.286362+00:00 [info] <0.228.0> Running boot step database defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:20.286533+00:00 [info] <0.228.0> Node database directory at /var/lib/rabbitmq/mnesia/rabbit@dc96961bdc36 is empty. Assuming we need to join an existing cluster or initialise from scratch...[0m
rabbitmq     | 2026-11-27 23:59:20.286583+00:00 [info] <0.228.0> Configured peer discovery backend: rabbit_peer_discovery_classic_config[0m
rabbitmq     | 2026-11-27 23:59:20.286607+00:00 [info] <0.228.0> Will try to lock with peer discovery backend rabbit_peer_discovery_classic_config[0m
rabbitmq     | 2026-11-27 23:59:20.286665+00:00 [info] <0.228.0> All discovered existing cluster peers:[0m
rabbitmq     | 2026-11-27 23:59:20.286686+00:00 [info] <0.228.0> Discovered no peer nodes to cluster with. Some discovery backends can filter nodes out based on a readiness criteria. Enabling debug logging might help troubleshoot.[0m
rabbitmq     | [38;5;87m2026-11-27 23:59:20.288456+00:00 [notice] <0.44.0> Application mnesia exited with reason: stopped[0m
rabbitmq     | 2026-11-27 23:59:20.401512+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:20.401644+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:20.410398+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:20.410502+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:20.410545+00:00 [info] <0.228.0> Feature flag `drop_unroutable_metric`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:20.410605+00:00 [info] <0.228.0> Feature flag `drop_unroutable_metric`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:20.411507+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.411546+00:00 [info] <0.228.0> Feature flags:   [~] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.411569+00:00 [info] <0.228.0> Feature flags:   [ ] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.411594+00:00 [info] <0.228.0> Feature flags:   [ ] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.411611+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.411639+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.411665+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.411682+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.411702+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.411720+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.420076+00:00 [info] <0.228.0> Feature flag `drop_unroutable_metric`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:20.421558+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.421602+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.421631+00:00 [info] <0.228.0> Feature flags:   [ ] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.421669+00:00 [info] <0.228.0> Feature flags:   [ ] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.421698+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.421733+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.421757+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.421791+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.421822+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.421843+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.428973+00:00 [info] <0.228.0> Feature flag `empty_basic_get_metric`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:20.429049+00:00 [info] <0.228.0> Feature flag `empty_basic_get_metric`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:20.430278+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.430345+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.430418+00:00 [info] <0.228.0> Feature flags:   [~] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.430439+00:00 [info] <0.228.0> Feature flags:   [ ] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.430469+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.430530+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.430569+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.430602+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.430624+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.430682+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.447638+00:00 [info] <0.228.0> Feature flag `empty_basic_get_metric`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:20.451744+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.451867+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.451953+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.452061+00:00 [info] <0.228.0> Feature flags:   [ ] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.452142+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.452223+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.452268+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.452332+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.452426+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.452478+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.470324+00:00 [info] <0.228.0> Feature flag `implicit_default_bindings`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:20.470475+00:00 [info] <0.228.0> Feature flag `implicit_default_bindings`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:20.472521+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.472602+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.472694+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.472781+00:00 [info] <0.228.0> Feature flags:   [~] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.472848+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.472975+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.473036+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.473079+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.473161+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.473247+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.491667+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 0 retries left[0m
rabbitmq     | 2026-11-27 23:59:20.491817+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:20.491973+00:00 [info] <0.228.0> Feature flag `implicit_default_bindings`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:20.493627+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.493680+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.493705+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.493731+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.493767+00:00 [info] <0.228.0> Feature flags:   [ ] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.493805+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.493831+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.493884+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.493917+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.493936+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.502436+00:00 [info] <0.228.0> Feature flag `maintenance_mode_status`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:20.502523+00:00 [info] <0.228.0> Feature flag `maintenance_mode_status`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:20.503419+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.503453+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.503479+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.503507+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.503525+00:00 [info] <0.228.0> Feature flags:   [~] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.503554+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.503574+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.503591+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.503611+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.503633+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.512502+00:00 [info] <0.228.0> Creating table rabbit_node_maintenance_states for feature flag `maintenance_mode_status`[0m
rabbitmq     | 2026-11-27 23:59:20.581997+00:00 [info] <0.228.0> Feature flag `maintenance_mode_status`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:20.583967+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.584023+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.584046+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.584073+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.584111+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.584138+00:00 [info] <0.228.0> Feature flags:   [ ] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.584164+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.584198+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.584232+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.584260+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.591449+00:00 [info] <0.228.0> Feature flag `quorum_queue`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:20.591522+00:00 [info] <0.228.0> Feature flag `quorum_queue`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:20.592888+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:20.593002+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:20.593070+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:20.593099+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:20.593145+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:20.593172+00:00 [info] <0.228.0> Feature flags:   [~] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:20.593206+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:20.593236+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:20.593267+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:20.593293+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:20.604389+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:20.604492+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:20.604519+00:00 [info] <0.228.0> Feature flag `quorum_queue`:   migrating Mnesia table rabbit_queue...[0m
rabbitmq     | 2026-11-27 23:59:20.783442+00:00 [info] <0.228.0> Feature flag `quorum_queue`:   migrating Mnesia table rabbit_durable_queue...[0m
rabbitmq     | 2026-11-27 23:59:21.104481+00:00 [info] <0.228.0> Feature flag `quorum_queue`:   Mnesia tables migration done[0m
rabbitmq     | 2026-11-27 23:59:21.104596+00:00 [info] <0.228.0> Feature flag `quorum_queue`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:21.107117+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.107196+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.107248+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.107321+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.107369+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.107440+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.107482+00:00 [info] <0.228.0> Feature flags:   [ ] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.107527+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.107582+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.107625+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.124039+00:00 [info] <0.228.0> Feature flag `stream_queue`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:21.124170+00:00 [info] <0.228.0> Feature flag `stream_queue`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:21.125346+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.125393+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.125478+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.125512+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.125552+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.125579+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.125614+00:00 [info] <0.228.0> Feature flags:   [~] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.125646+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.125674+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.125707+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.136734+00:00 [info] <0.228.0> Feature flag `stream_queue`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:21.138269+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.138318+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.138352+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.138388+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.138444+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.138555+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.138597+00:00 [info] <0.228.0> Feature flags:   [x] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.138645+00:00 [info] <0.228.0> Feature flags:   [ ] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.138674+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.138706+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.147086+00:00 [info] <0.228.0> Feature flag `user_limits`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:21.147181+00:00 [info] <0.228.0> Feature flag `user_limits`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:21.148364+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.148409+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.148458+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.148494+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.148522+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.148562+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.148593+00:00 [info] <0.228.0> Feature flags:   [x] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.148619+00:00 [info] <0.228.0> Feature flags:   [~] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.148652+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.148690+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.159378+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:21.159499+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:21.175786+00:00 [info] <0.228.0> Feature flag `user_limits`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:21.177716+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.177766+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.177819+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.177889+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.177921+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.177952+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.177976+00:00 [info] <0.228.0> Feature flags:   [x] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.178003+00:00 [info] <0.228.0> Feature flags:   [x] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.178050+00:00 [info] <0.228.0> Feature flags:   [ ] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.178080+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.187905+00:00 [info] <0.228.0> Feature flag `virtual_host_metadata`: supported, attempt to enable...[0m
rabbitmq     | 2026-11-27 23:59:21.187990+00:00 [info] <0.228.0> Feature flag `virtual_host_metadata`: mark as enabled=state_changing[0m
rabbitmq     | 2026-11-27 23:59:21.189062+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.189117+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.189141+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.189160+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.189177+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.189197+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.189225+00:00 [info] <0.228.0> Feature flags:   [x] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.189241+00:00 [info] <0.228.0> Feature flags:   [x] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.189257+00:00 [info] <0.228.0> Feature flags:   [~] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.189275+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.204611+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:21.204714+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:21.220387+00:00 [info] <0.228.0> Feature flag `virtual_host_metadata`: mark as enabled=true[0m
rabbitmq     | 2026-11-27 23:59:21.221994+00:00 [info] <0.228.0> Feature flags: list of feature flags found:[0m
rabbitmq     | 2026-11-27 23:59:21.222035+00:00 [info] <0.228.0> Feature flags:   [x] drop_unroutable_metric[0m
rabbitmq     | 2026-11-27 23:59:21.222055+00:00 [info] <0.228.0> Feature flags:   [x] empty_basic_get_metric[0m
rabbitmq     | 2026-11-27 23:59:21.222085+00:00 [info] <0.228.0> Feature flags:   [x] implicit_default_bindings[0m
rabbitmq     | 2026-11-27 23:59:21.222125+00:00 [info] <0.228.0> Feature flags:   [x] maintenance_mode_status[0m
rabbitmq     | 2026-11-27 23:59:21.222142+00:00 [info] <0.228.0> Feature flags:   [x] quorum_queue[0m
rabbitmq     | 2026-11-27 23:59:21.222158+00:00 [info] <0.228.0> Feature flags:   [x] stream_queue[0m
rabbitmq     | 2026-11-27 23:59:21.222205+00:00 [info] <0.228.0> Feature flags:   [x] user_limits[0m
rabbitmq     | 2026-11-27 23:59:21.222223+00:00 [info] <0.228.0> Feature flags:   [x] virtual_host_metadata[0m
rabbitmq     | 2026-11-27 23:59:21.222240+00:00 [info] <0.228.0> Feature flags: feature flag states written to disk: yes[0m
rabbitmq     | 2026-11-27 23:59:21.235387+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:21.235581+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:21.246381+00:00 [info] <0.228.0> Waiting for Mnesia tables for 30000 ms, 9 retries left[0m
rabbitmq     | 2026-11-27 23:59:21.246504+00:00 [info] <0.228.0> Successfully synced tables from a peer[0m
rabbitmq     | 2026-11-27 23:59:21.246537+00:00 [info] <0.228.0> Peer discovery backend rabbit_peer_discovery_classic_config does not support registration, skipping registration.[0m
rabbitmq     | 2026-11-27 23:59:21.246571+00:00 [info] <0.228.0> Will try to unlock with peer discovery backend rabbit_peer_discovery_classic_config[0m
rabbitmq     | 2026-11-27 23:59:21.246639+00:00 [info] <0.228.0> Running boot step database_sync defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.246746+00:00 [info] <0.228.0> Running boot step feature_flags defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.246886+00:00 [info] <0.228.0> Running boot step codec_correctness_check defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.246918+00:00 [info] <0.228.0> Running boot step external_infrastructure defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.246936+00:00 [info] <0.228.0> Running boot step rabbit_registry defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247061+00:00 [info] <0.228.0> Running boot step rabbit_auth_mechanism_cr_demo defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247211+00:00 [info] <0.228.0> Running boot step rabbit_queue_location_random defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247374+00:00 [info] <0.228.0> Running boot step rabbit_event defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247553+00:00 [info] <0.228.0> Running boot step rabbit_auth_mechanism_amqplain defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247629+00:00 [info] <0.228.0> Running boot step rabbit_auth_mechanism_plain defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247705+00:00 [info] <0.228.0> Running boot step rabbit_exchange_type_direct defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247762+00:00 [info] <0.228.0> Running boot step rabbit_exchange_type_fanout defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247817+00:00 [info] <0.228.0> Running boot step rabbit_exchange_type_headers defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247891+00:00 [info] <0.228.0> Running boot step rabbit_exchange_type_topic defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.247952+00:00 [info] <0.228.0> Running boot step rabbit_mirror_queue_mode_all defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248016+00:00 [info] <0.228.0> Running boot step rabbit_mirror_queue_mode_exactly defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248079+00:00 [info] <0.228.0> Running boot step rabbit_mirror_queue_mode_nodes defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248151+00:00 [info] <0.228.0> Running boot step rabbit_priority_queue defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248183+00:00 [info] <0.228.0> Priority queues enabled, real BQ is rabbit_variable_queue[0m
rabbitmq     | 2026-11-27 23:59:21.248230+00:00 [info] <0.228.0> Running boot step rabbit_queue_location_client_local defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248311+00:00 [info] <0.228.0> Running boot step rabbit_queue_location_min_masters defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248404+00:00 [info] <0.228.0> Running boot step kernel_ready defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248487+00:00 [info] <0.228.0> Running boot step rabbit_sysmon_minder defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.248653+00:00 [info] <0.228.0> Running boot step rabbit_epmd_monitor defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.249370+00:00 [info] <0.572.0> epmd monitor knows us, inter-node communication (distribution) port: 25672[0m
rabbitmq     | 2026-11-27 23:59:21.249457+00:00 [info] <0.228.0> Running boot step guid_generator defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.250976+00:00 [info] <0.228.0> Running boot step rabbit_node_monitor defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.251120+00:00 [info] <0.576.0> Starting rabbit_node_monitor[0m
rabbitmq     | 2026-11-27 23:59:21.251222+00:00 [info] <0.228.0> Running boot step delegate_sup defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.251752+00:00 [info] <0.228.0> Running boot step rabbit_memory_monitor defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.251983+00:00 [info] <0.228.0> Running boot step core_initialized defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.252026+00:00 [info] <0.228.0> Running boot step upgrade_queues defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.260152+00:00 [info] <0.228.0> message_store upgrades: 1 to apply[0m
rabbitmq     | 2026-11-27 23:59:21.260281+00:00 [info] <0.228.0> message_store upgrades: Applying rabbit_variable_queue:move_messages_to_vhost_store[0m
rabbitmq     | 2026-11-27 23:59:21.260436+00:00 [info] <0.228.0> message_store upgrades: No durable queues found. Skipping message store migration[0m
rabbitmq     | 2026-11-27 23:59:21.260484+00:00 [info] <0.228.0> message_store upgrades: Removing the old message store data[0m
rabbitmq     | 2026-11-27 23:59:21.260979+00:00 [info] <0.228.0> message_store upgrades: All upgrades applied successfully[0m
rabbitmq     | 2026-11-27 23:59:21.273330+00:00 [info] <0.228.0> Running boot step channel_tracking defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.276874+00:00 [info] <0.228.0> Setting up a table for channel tracking on this node: tracked_channel_on_node_rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:21.281037+00:00 [info] <0.228.0> Setting up a table for channel tracking on this node: tracked_channel_table_per_user_on_node_rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:21.281264+00:00 [info] <0.228.0> Running boot step rabbit_channel_tracking_handler defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.281355+00:00 [info] <0.228.0> Running boot step connection_tracking defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.283954+00:00 [info] <0.228.0> Setting up a table for connection tracking on this node: tracked_connection_on_node_rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:21.289732+00:00 [info] <0.228.0> Setting up a table for per-vhost connection counting on this node: tracked_connection_per_vhost_on_node_rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:21.292324+00:00 [info] <0.228.0> Setting up a table for per-user connection counting on this node: tracked_connection_table_per_user_on_node_rabbit@dc96961bdc36[0m
rabbitmq     | 2026-11-27 23:59:21.292549+00:00 [info] <0.228.0> Running boot step rabbit_connection_tracking_handler defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.292619+00:00 [info] <0.228.0> Running boot step rabbit_exchange_parameters defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.292690+00:00 [info] <0.228.0> Running boot step rabbit_mirror_queue_misc defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.292851+00:00 [info] <0.228.0> Running boot step rabbit_policies defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.293214+00:00 [info] <0.228.0> Running boot step rabbit_policy defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.293275+00:00 [info] <0.228.0> Running boot step rabbit_queue_location_validator defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.293317+00:00 [info] <0.228.0> Running boot step rabbit_quorum_memory_manager defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.293372+00:00 [info] <0.228.0> Running boot step rabbit_stream_coordinator defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.293474+00:00 [info] <0.228.0> Running boot step rabbit_vhost_limit defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.293560+00:00 [info] <0.228.0> Running boot step rabbit_mgmt_reset_handler defined by app rabbitmq_management[0m
rabbitmq     | 2026-11-27 23:59:21.293634+00:00 [info] <0.228.0> Running boot step rabbit_mgmt_db_handler defined by app rabbitmq_management_agent[0m
rabbitmq     | 2026-11-27 23:59:21.293681+00:00 [info] <0.228.0> Management plugin: using rates mode 'basic'[0m
rabbitmq     | 2026-11-27 23:59:21.294060+00:00 [info] <0.228.0> Running boot step recovery defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.295145+00:00 [info] <0.228.0> Running boot step empty_db_check defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.295186+00:00 [info] <0.228.0> Will seed default virtual host and user...[0m
rabbitmq     | 2026-11-27 23:59:21.295366+00:00 [info] <0.228.0> Adding vhost '/' (description: 'Default virtual host', tags: [])[0m
rabbitmq     | 2026-11-27 23:59:21.320864+00:00 [info] <0.637.0> Making sure data directory '/var/lib/rabbitmq/mnesia/rabbit@dc96961bdc36/msg_stores/vhosts/628WB79CIFDYO9LJI6DKMI09L' for vhost '/' exists[0m
rabbitmq     | 2026-11-27 23:59:21.321997+00:00 [info] <0.637.0> Setting segment_entry_count for vhost '/' with 0 queues to '2048'[0m
rabbitmq     | 2026-11-27 23:59:21.329756+00:00 [info] <0.637.0> Starting message stores for vhost '/'[0m
rabbitmq     | 2026-11-27 23:59:21.330086+00:00 [info] <0.641.0> Message store "628WB79CIFDYO9LJI6DKMI09L/msg_store_transient": using rabbit_msg_store_ets_index to provide index[0m
rabbitmq     | 2026-11-27 23:59:21.333745+00:00 [info] <0.637.0> Started message store of type transient for vhost '/'[0m
rabbitmq     | 2026-11-27 23:59:21.333923+00:00 [info] <0.645.0> Message store "628WB79CIFDYO9LJI6DKMI09L/msg_store_persistent": using rabbit_msg_store_ets_index to provide index[0m
rabbitmq     | [38;5;214m2026-11-27 23:59:21.334756+00:00 [warning] <0.645.0> Message store "628WB79CIFDYO9LJI6DKMI09L/msg_store_persistent": rebuilding indices from scratch[0m
rabbitmq     | 2026-11-27 23:59:21.335987+00:00 [info] <0.637.0> Started message store of type persistent for vhost '/'[0m
rabbitmq     | 2026-11-27 23:59:21.336126+00:00 [info] <0.637.0> Recovering 0 queues of type rabbit_classic_queue took 13ms[0m
rabbitmq     | 2026-11-27 23:59:21.336182+00:00 [info] <0.637.0> Recovering 0 queues of type rabbit_quorum_queue took 0ms[0m
rabbitmq     | 2026-11-27 23:59:21.336220+00:00 [info] <0.637.0> Recovering 0 queues of type rabbit_stream_queue took 0ms[0m
rabbitmq     | 2026-11-27 23:59:21.341991+00:00 [info] <0.228.0> Created user 'guest'[0m
rabbitmq     | 2026-11-27 23:59:21.343954+00:00 [info] <0.228.0> Successfully set user tags for user 'guest' to [administrator][0m
rabbitmq     | 2026-11-27 23:59:21.345208+00:00 [info] <0.228.0> Successfully set permissions for 'guest' in virtual host '/' to '.*', '.*', '.*'[0m
rabbitmq     | 2026-11-27 23:59:21.345284+00:00 [info] <0.228.0> Running boot step rabbit_looking_glass defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.345312+00:00 [info] <0.228.0> Running boot step rabbit_core_metrics_gc defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.345499+00:00 [info] <0.228.0> Running boot step background_gc defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.345742+00:00 [info] <0.228.0> Running boot step routing_ready defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.345858+00:00 [info] <0.228.0> Running boot step pre_flight defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.345926+00:00 [info] <0.228.0> Running boot step notify_cluster defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.345988+00:00 [info] <0.228.0> Running boot step networking defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.346054+00:00 [info] <0.228.0> Running boot step definition_import_worker_pool defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.346146+00:00 [info] <0.285.0> Starting worker pool 'definition_import_pool' with 12 processes in it[0m
rabbitmq     | 2026-11-27 23:59:21.347001+00:00 [info] <0.228.0> Running boot step cluster_name defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.347076+00:00 [info] <0.228.0> Initialising internal cluster ID to 'rabbitmq-cluster-id-sOxUjbhK0I-148I4R0xeJw'[0m
rabbitmq     | 2026-11-27 23:59:21.348293+00:00 [info] <0.228.0> Running boot step direct_client defined by app rabbit[0m
rabbitmq     | 2026-11-27 23:59:21.348424+00:00 [info] <0.228.0> Running boot step rabbit_management_load_definitions defined by app rabbitmq_management[0m
rabbitmq     | 2026-11-27 23:59:21.348619+00:00 [info] <0.686.0> Resetting node maintenance status[0m
rabbitmq     | 2026-11-27 23:59:21.372366+00:00 [info] <0.745.0> Management plugin: HTTP (non-TLS) listener started on port 15672[0m
rabbitmq     | 2026-11-27 23:59:21.372514+00:00 [info] <0.777.0> Statistics database started.[0m
rabbitmq     | 2026-11-27 23:59:21.372590+00:00 [info] <0.776.0> Starting worker pool 'management_worker_pool' with 3 processes in it[0m
rabbitmq     | 2026-11-27 23:59:21.389722+00:00 [info] <0.791.0> Prometheus metrics: HTTP (non-TLS) listener started on port 15692[0m
rabbitmq     | 2026-11-27 23:59:21.389857+00:00 [info] <0.686.0> Ready to start client connection listeners[0m
rabbitmq     | 2026-11-27 23:59:21.391397+00:00 [info] <0.835.0> started TCP listener on [::]:5672[0m
rabbitmq     |  completed with 4 plugins.
rabbitmq     | 2026-11-27 23:59:21.451274+00:00 [info] <0.686.0> Server startup complete; 4 plugins started.[0m
rabbitmq     | 2026-11-27 23:59:21.451274+00:00 [info] <0.686.0>  * rabbitmq_prometheus[0m
rabbitmq     | 2026-11-27 23:59:21.451274+00:00 [info] <0.686.0>  * rabbitmq_management[0m
rabbitmq     | 2026-11-27 23:59:21.451274+00:00 [info] <0.686.0>  * rabbitmq_web_dispatch[0m
rabbitmq     | 2026-11-27 23:59:21.451274+00:00 [info] <0.686.0>  * rabbitmq_management_agent[0m
rabbitmq     | 2026-11-27 23:59:28.278258+00:00 [info] <0.858.0> accepting AMQP connection <0.858.0> (192.168.96.3:44414 -> 192.168.96.2:5672)[0m
rabbitmq     | 2026-11-27 23:59:28.281541+00:00 [info] <0.858.0> connection <0.858.0> (192.168.96.3:44414 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.642786+00:00 [info] <0.874.0> accepting AMQP connection <0.874.0> (192.168.96.4:35966 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.645392+00:00 [info] <0.874.0> connection <0.874.0> (192.168.96.4:35966 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.653656+00:00 [info] <0.890.0> accepting AMQP connection <0.890.0> (192.168.96.4:41648 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.655585+00:00 [info] <0.890.0> connection <0.890.0> (192.168.96.4:41648 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.659683+00:00 [info] <0.901.0> accepting AMQP connection <0.901.0> (192.168.96.4:41650 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.661531+00:00 [info] <0.901.0> connection <0.901.0> (192.168.96.4:41650 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.669409+00:00 [info] <0.917.0> accepting AMQP connection <0.917.0> (192.168.96.4:41656 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.670986+00:00 [info] <0.917.0> connection <0.917.0> (192.168.96.4:41656 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.677305+00:00 [info] <0.933.0> accepting AMQP connection <0.933.0> (192.168.96.4:41666 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.678761+00:00 [info] <0.933.0> connection <0.933.0> (192.168.96.4:41666 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.685195+00:00 [info] <0.949.0> accepting AMQP connection <0.949.0> (192.168.96.4:41674 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.686678+00:00 [info] <0.949.0> connection <0.949.0> (192.168.96.4:41674 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:28.693589+00:00 [info] <0.965.0> accepting AMQP connection <0.965.0> (192.168.96.4:41688 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:28.695021+00:00 [info] <0.965.0> connection <0.965.0> (192.168.96.4:41688 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.411686+00:00 [info] <0.981.0> accepting AMQP connection <0.981.0> (192.168.96.5:46560 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.413814+00:00 [info] <0.981.0> connection <0.981.0> (192.168.96.5:46560 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.421181+00:00 [info] <0.997.0> accepting AMQP connection <0.997.0> (192.168.96.5:46572 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.422600+00:00 [info] <0.997.0> connection <0.997.0> (192.168.96.5:46572 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.426451+00:00 [info] <0.1008.0> accepting AMQP connection <0.1008.0> (192.168.96.5:46586 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.427964+00:00 [info] <0.1008.0> connection <0.1008.0> (192.168.96.5:46586 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.431311+00:00 [info] <0.1019.0> accepting AMQP connection <0.1019.0> (192.168.96.5:46602 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.432723+00:00 [info] <0.1019.0> connection <0.1019.0> (192.168.96.5:46602 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.437065+00:00 [info] <0.1030.0> accepting AMQP connection <0.1030.0> (192.168.96.5:46610 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.439742+00:00 [info] <0.1030.0> connection <0.1030.0> (192.168.96.5:46610 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.443228+00:00 [info] <0.1041.0> accepting AMQP connection <0.1041.0> (192.168.96.5:46614 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.444582+00:00 [info] <0.1041.0> connection <0.1041.0> (192.168.96.5:46614 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:29.447740+00:00 [info] <0.1052.0> accepting AMQP connection <0.1052.0> (192.168.96.5:46620 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:29.449111+00:00 [info] <0.1052.0> connection <0.1052.0> (192.168.96.5:46620 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.121125+00:00 [info] <0.1063.0> accepting AMQP connection <0.1063.0> (192.168.96.6:52316 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.123182+00:00 [info] <0.1063.0> connection <0.1063.0> (192.168.96.6:52316 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.130003+00:00 [info] <0.1079.0> accepting AMQP connection <0.1079.0> (192.168.96.6:52318 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.146129+00:00 [info] <0.1079.0> connection <0.1079.0> (192.168.96.6:52318 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.152382+00:00 [info] <0.1090.0> accepting AMQP connection <0.1090.0> (192.168.96.6:52326 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.163115+00:00 [info] <0.1090.0> connection <0.1090.0> (192.168.96.6:52326 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.168593+00:00 [info] <0.1101.0> accepting AMQP connection <0.1101.0> (192.168.96.6:52336 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.174394+00:00 [info] <0.1101.0> connection <0.1101.0> (192.168.96.6:52336 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.181674+00:00 [info] <0.1112.0> accepting AMQP connection <0.1112.0> (192.168.96.6:52344 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.183565+00:00 [info] <0.1112.0> connection <0.1112.0> (192.168.96.6:52344 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.187253+00:00 [info] <0.1123.0> accepting AMQP connection <0.1123.0> (192.168.96.6:52360 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.189559+00:00 [info] <0.1123.0> connection <0.1123.0> (192.168.96.6:52360 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.193372+00:00 [info] <0.1134.0> accepting AMQP connection <0.1134.0> (192.168.96.6:52370 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.195220+00:00 [info] <0.1134.0> connection <0.1134.0> (192.168.96.6:52370 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.561146+00:00 [info] <0.1146.0> accepting AMQP connection <0.1146.0> (192.168.96.3:45142 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.567549+00:00 [info] <0.1146.0> connection <0.1146.0> (192.168.96.3:45142 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.580081+00:00 [info] <0.1157.0> accepting AMQP connection <0.1157.0> (192.168.96.3:45154 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.588705+00:00 [info] <0.1157.0> connection <0.1157.0> (192.168.96.3:45154 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:30.601819+00:00 [info] <0.1168.0> accepting AMQP connection <0.1168.0> (192.168.96.3:45156 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:30.607072+00:00 [info] <0.1168.0> connection <0.1168.0> (192.168.96.3:45156 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1       | INIICIII
rabbitmq        | 2026-11-27 23:59:31.310332+00:00 [info] <0.1179.0> accepting AMQP connection <0.1179.0> (192.168.96.8:44278 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:31.312983+00:00 [info] <0.1179.0> connection <0.1179.0> (192.168.96.8:44278 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:31.327441+00:00 [info] <0.1195.0> accepting AMQP connection <0.1195.0> (192.168.96.8:44292 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:31.329943+00:00 [info] <0.1195.0> connection <0.1195.0> (192.168.96.8:44292 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:31.338950+00:00 [info] <0.1211.0> accepting AMQP connection <0.1211.0> (192.168.96.8:44306 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:31.342199+00:00 [info] <0.1211.0> connection <0.1211.0> (192.168.96.8:44306 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq        | 2026-11-27 23:59:31.354857+00:00 [info] <0.1227.0> accepting AMQP connection <0.1227.0> (192.168.96.8:44314 -> 192.168.96.2:5672)[0m
rabbitmq        | 2026-11-27 23:59:31.360705+00:00 [info] <0.1227.0> connection <0.1227.0> (192.168.96.8:44314 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1       | {}
sum_top_1       | {}
rabbitmq         | 2026-11-27 23:59:31.536637+00:00 [info] <0.1243.0> accepting AMQP connection <0.1243.0> (192.168.96.9:46016 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.542161+00:00 [info] <0.1243.0> connection <0.1243.0> (192.168.96.9:46016 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.550073+00:00 [info] <0.1254.0> accepting AMQP connection <0.1254.0> (192.168.96.9:46018 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.556776+00:00 [info] <0.1254.0> connection <0.1254.0> (192.168.96.9:46018 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.580671+00:00 [info] <0.1270.0> accepting AMQP connection <0.1270.0> (192.168.96.9:46034 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.605268+00:00 [info] <0.1270.0> connection <0.1270.0> (192.168.96.9:46034 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.624743+00:00 [info] <0.1286.0> accepting AMQP connection <0.1286.0> (192.168.96.9:46046 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.628798+00:00 [info] <0.1286.0> connection <0.1286.0> (192.168.96.9:46046 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.643224+00:00 [info] <0.1302.0> accepting AMQP connection <0.1302.0> (192.168.96.9:46058 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.645070+00:00 [info] <0.1302.0> connection <0.1302.0> (192.168.96.9:46058 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_2        | INIICIII
rabbitmq         | 2026-11-27 23:59:31.874610+00:00 [info] <0.1313.0> accepting AMQP connection <0.1313.0> (192.168.96.12:38126 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.878925+00:00 [info] <0.1313.0> connection <0.1313.0> (192.168.96.12:38126 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.890650+00:00 [info] <0.1329.0> accepting AMQP connection <0.1329.0> (192.168.96.12:38132 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.897912+00:00 [info] <0.1329.0> connection <0.1329.0> (192.168.96.12:38132 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.908270+00:00 [info] <0.1340.0> accepting AMQP connection <0.1340.0> (192.168.96.12:38142 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.912358+00:00 [info] <0.1340.0> connection <0.1340.0> (192.168.96.12:38142 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:31.931923+00:00 [info] <0.1351.0> accepting AMQP connection <0.1351.0> (192.168.96.12:38144 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:31.933939+00:00 [info] <0.1351.0> connection <0.1351.0> (192.168.96.12:38144 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_2        | {}
sum_top_2        | {}
rabbitmq         | 2026-11-27 23:59:32.042346+00:00 [info] <0.1363.0> accepting AMQP connection <0.1363.0> (192.168.96.10:39392 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.059166+00:00 [info] <0.1366.0> accepting AMQP connection <0.1366.0> (192.168.96.11:57156 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.074262+00:00 [info] <0.1363.0> connection <0.1363.0> (192.168.96.10:39392 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.074475+00:00 [info] <0.1366.0> connection <0.1366.0> (192.168.96.11:57156 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.095114+00:00 [info] <0.1385.0> accepting AMQP connection <0.1385.0> (192.168.96.11:57162 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.098594+00:00 [info] <0.1385.0> connection <0.1385.0> (192.168.96.11:57162 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.100221+00:00 [info] <0.1396.0> accepting AMQP connection <0.1396.0> (192.168.96.10:39408 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.125914+00:00 [info] <0.1396.0> connection <0.1396.0> (192.168.96.10:39408 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.152725+00:00 [info] <0.1415.0> accepting AMQP connection <0.1415.0> (192.168.96.11:57168 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.153151+00:00 [info] <0.1412.0> accepting AMQP connection <0.1412.0> (192.168.96.10:39418 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.163183+00:00 [info] <0.1415.0> connection <0.1415.0> (192.168.96.11:57168 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.163325+00:00 [info] <0.1412.0> connection <0.1412.0> (192.168.96.10:39418 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.176540+00:00 [info] <0.1434.0> accepting AMQP connection <0.1434.0> (192.168.96.11:57180 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.177247+00:00 [info] <0.1437.0> accepting AMQP connection <0.1437.0> (192.168.96.10:39432 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.188430+00:00 [info] <0.1434.0> connection <0.1434.0> (192.168.96.11:57180 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.190807+00:00 [info] <0.1437.0> connection <0.1437.0> (192.168.96.10:39432 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.199338+00:00 [info] <0.1456.0> accepting AMQP connection <0.1456.0> (192.168.96.11:57194 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.203182+00:00 [info] <0.1459.0> accepting AMQP connection <0.1459.0> (192.168.96.10:39446 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.212974+00:00 [info] <0.1459.0> connection <0.1459.0> (192.168.96.10:39446 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.215927+00:00 [info] <0.1456.0> connection <0.1456.0> (192.168.96.11:57194 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.252894+00:00 [info] <0.1487.0> accepting AMQP connection <0.1487.0> (192.168.96.10:39448 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.253109+00:00 [info] <0.1490.0> accepting AMQP connection <0.1490.0> (192.168.96.11:57208 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.256602+00:00 [info] <0.1490.0> connection <0.1490.0> (192.168.96.11:57208 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.258276+00:00 [info] <0.1487.0> connection <0.1487.0> (192.168.96.10:39448 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.308760+00:00 [info] <0.1514.0> accepting AMQP connection <0.1514.0> (192.168.96.11:57220 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.309114+00:00 [info] <0.1517.0> accepting AMQP connection <0.1517.0> (192.168.96.10:39464 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.312968+00:00 [info] <0.1514.0> connection <0.1514.0> (192.168.96.11:57220 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.315314+00:00 [info] <0.1517.0> connection <0.1517.0> (192.168.96.10:39464 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.321855+00:00 [info] <0.1543.0> accepting AMQP connection <0.1543.0> (192.168.96.14:45986 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.326204+00:00 [info] <0.1543.0> connection <0.1543.0> (192.168.96.14:45986 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.336623+00:00 [info] <0.1556.0> accepting AMQP connection <0.1556.0> (192.168.96.10:39480 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.337164+00:00 [info] <0.1559.0> accepting AMQP connection <0.1559.0> (192.168.96.14:45996 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.338518+00:00 [info] <0.1562.0> accepting AMQP connection <0.1562.0> (192.168.96.11:57224 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.343897+00:00 [info] <0.1556.0> connection <0.1556.0> (192.168.96.10:39480 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.344430+00:00 [info] <0.1559.0> connection <0.1559.0> (192.168.96.14:45996 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.348026+00:00 [info] <0.1562.0> connection <0.1562.0> (192.168.96.11:57224 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.380239+00:00 [info] <0.1593.0> accepting AMQP connection <0.1593.0> (192.168.96.13:49334 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.385507+00:00 [info] <0.1593.0> connection <0.1593.0> (192.168.96.13:49334 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.396444+00:00 [info] <0.1605.0> accepting AMQP connection <0.1605.0> (192.168.96.13:49348 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.407743+00:00 [info] <0.1605.0> connection <0.1605.0> (192.168.96.13:49348 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.416500+00:00 [info] <0.1616.0> accepting AMQP connection <0.1616.0> (192.168.96.13:49362 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.420714+00:00 [info] <0.1616.0> connection <0.1616.0> (192.168.96.13:49362 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.427716+00:00 [info] <0.1627.0> accepting AMQP connection <0.1627.0> (192.168.96.13:49368 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.431656+00:00 [info] <0.1627.0> connection <0.1627.0> (192.168.96.13:49368 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.433873+00:00 [info] <0.1638.0> accepting AMQP connection <0.1638.0> (192.168.96.11:57232 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.434223+00:00 [info] <0.1641.0> accepting AMQP connection <0.1641.0> (192.168.96.10:39496 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.437934+00:00 [info] <0.1644.0> accepting AMQP connection <0.1644.0> (192.168.96.13:49372 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.443645+00:00 [info] <0.1644.0> connection <0.1644.0> (192.168.96.13:49372 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.443629+00:00 [info] <0.1638.0> connection <0.1638.0> (192.168.96.11:57232 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.445296+00:00 [info] <0.1641.0> connection <0.1641.0> (192.168.96.10:39496 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.492443+00:00 [info] <0.1680.0> accepting AMQP connection <0.1680.0> (192.168.96.10:39512 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.492863+00:00 [info] <0.1683.0> accepting AMQP connection <0.1683.0> (192.168.96.11:57234 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.495043+00:00 [info] <0.1680.0> connection <0.1680.0> (192.168.96.10:39512 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.495312+00:00 [info] <0.1683.0> connection <0.1683.0> (192.168.96.11:57234 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
rabbitmq         | 2026-11-27 23:59:32.672615+00:00 [info] <0.1707.0> accepting AMQP connection <0.1707.0> (192.168.96.16:37206 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:32.697003+00:00 [info] <0.1707.0> connection <0.1707.0> (192.168.96.16:37206 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:32.706555+00:00 [info] <0.1718.0> accepting AMQP connection <0.1718.0> (192.168.96.16:37208 -> 192.168.96.2:5672)[0m
sum_top_1        | llega msg
sum_top_1        | procesado
rabbitmq         | 2026-11-27 23:59:32.718719+00:00 [info] <0.1718.0> connection <0.1718.0> (192.168.96.16:37208 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1        | listo
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
rabbitmq         | 2026-11-27 23:59:33.158429+00:00 [info] <0.1730.0> accepting AMQP connection <0.1730.0> (192.168.96.15:50038 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:33.166443+00:00 [info] <0.1730.0> connection <0.1730.0> (192.168.96.15:50038 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:33.172119+00:00 [info] <0.1741.0> accepting AMQP connection <0.1741.0> (192.168.96.15:50050 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:33.178252+00:00 [info] <0.1741.0> connection <0.1741.0> (192.168.96.15:50050 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:33.196778+00:00 [info] <0.1752.0> accepting AMQP connection <0.1752.0> (192.168.96.15:50052 -> 192.168.96.2:5672)[0m
sum_top_1        | llega msg
sum_top_1        | procesado
rabbitmq         | 2026-11-27 23:59:33.200196+00:00 [info] <0.1752.0> connection <0.1752.0> (192.168.96.15:50052 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1        | listo
rabbitmq         | 2026-11-27 23:59:33.217388+00:00 [info] <0.1763.0> accepting AMQP connection <0.1763.0> (192.168.96.15:50060 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:33.221462+00:00 [info] <0.1763.0> connection <0.1763.0> (192.168.96.15:50060 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:33.228361+00:00 [info] <0.1774.0> accepting AMQP connection <0.1774.0> (192.168.96.15:50064 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:33.228351+00:00 [info] <0.1777.0> accepting AMQP connection <0.1777.0> (192.168.96.17:52048 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:33.230237+00:00 [info] <0.1774.0> connection <0.1774.0> (192.168.96.15:50064 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:33.231702+00:00 [info] <0.1777.0> connection <0.1777.0> (192.168.96.17:52048 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq         | 2026-11-27 23:59:33.244185+00:00 [info] <0.1796.0> accepting AMQP connection <0.1796.0> (192.168.96.17:52054 -> 192.168.96.2:5672)[0m
rabbitmq         | 2026-11-27 23:59:33.250197+00:00 [info] <0.1796.0> connection <0.1796.0> (192.168.96.17:52054 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
sum_top_1        | llega msg
sum_top_1        | procesado
sum_top_1        | listo
sum_top_1        | ckpt
sum_top_1        | end
rabbitmq           | 2026-11-27 23:59:33.643406+00:00 [info] <0.1822.0> accepting AMQP connection <0.1822.0> (192.168.96.19:49058 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.645952+00:00 [info] <0.1822.0> connection <0.1822.0> (192.168.96.19:49058 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.652987+00:00 [info] <0.1833.0> accepting AMQP connection <0.1833.0> (192.168.96.19:49066 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.655077+00:00 [info] <0.1833.0> connection <0.1833.0> (192.168.96.19:49066 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
rabbitmq           | 2026-11-27 23:59:33.731597+00:00 [info] <0.1844.0> accepting AMQP connection <0.1844.0> (192.168.96.18:35786 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.734513+00:00 [info] <0.1844.0> connection <0.1844.0> (192.168.96.18:35786 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.735990+00:00 [info] <0.1850.0> accepting AMQP connection <0.1850.0> (192.168.96.20:53214 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.738388+00:00 [info] <0.1850.0> connection <0.1850.0> (192.168.96.20:53214 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.741568+00:00 [info] <0.1866.0> accepting AMQP connection <0.1866.0> (192.168.96.18:35798 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.744596+00:00 [info] <0.1866.0> connection <0.1866.0> (192.168.96.18:35798 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
rabbitmq           | 2026-11-27 23:59:33.784714+00:00 [info] <0.1877.0> accepting AMQP connection <0.1877.0> (192.168.96.20:53222 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.785065+00:00 [info] <0.1880.0> accepting AMQP connection <0.1880.0> (192.168.96.18:35800 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.791137+00:00 [info] <0.1877.0> connection <0.1877.0> (192.168.96.20:53222 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.798184+00:00 [info] <0.1880.0> connection <0.1880.0> (192.168.96.18:35800 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.811105+00:00 [info] <0.1899.0> accepting AMQP connection <0.1899.0> (192.168.96.18:35808 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.817900+00:00 [info] <0.1899.0> connection <0.1899.0> (192.168.96.18:35808 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.850515+00:00 [info] <0.1910.0> accepting AMQP connection <0.1910.0> (192.168.96.18:35816 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.862090+00:00 [info] <0.1910.0> connection <0.1910.0> (192.168.96.18:35816 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.870435+00:00 [info] <0.1921.0> accepting AMQP connection <0.1921.0> (192.168.96.18:35830 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.877218+00:00 [info] <0.1921.0> connection <0.1921.0> (192.168.96.18:35830 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.894392+00:00 [info] <0.1932.0> accepting AMQP connection <0.1932.0> (192.168.96.18:35846 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.897211+00:00 [info] <0.1932.0> connection <0.1932.0> (192.168.96.18:35846 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.903748+00:00 [info] <0.1943.0> accepting AMQP connection <0.1943.0> (192.168.96.18:35850 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.907315+00:00 [info] <0.1943.0> connection <0.1943.0> (192.168.96.18:35850 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1          | llega msg
sum_top_1          | procesado
rabbitmq           | 2026-11-27 23:59:33.914861+00:00 [info] <0.1954.0> accepting AMQP connection <0.1954.0> (192.168.96.18:35864 -> 192.168.96.2:5672)[0m
sum_top_1          | listo
rabbitmq           | 2026-11-27 23:59:33.923989+00:00 [info] <0.1954.0> connection <0.1954.0> (192.168.96.18:35864 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.928414+00:00 [info] <0.1965.0> accepting AMQP connection <0.1965.0> (192.168.96.18:35868 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.930416+00:00 [info] <0.1965.0> connection <0.1965.0> (192.168.96.18:35868 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_0          | INIICIII
rabbitmq           | 2026-11-27 23:59:33.986241+00:00 [info] <0.1976.0> accepting AMQP connection <0.1976.0> (192.168.96.21:60008 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.988515+00:00 [info] <0.1976.0> connection <0.1976.0> (192.168.96.21:60008 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.992714+00:00 [info] <0.1987.0> accepting AMQP connection <0.1987.0> (192.168.96.21:60010 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.994213+00:00 [info] <0.1987.0> connection <0.1987.0> (192.168.96.21:60010 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:33.997627+00:00 [info] <0.1998.0> accepting AMQP connection <0.1998.0> (192.168.96.21:60014 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:33.999030+00:00 [info] <0.1998.0> connection <0.1998.0> (192.168.96.21:60014 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:34.002241+00:00 [info] <0.2009.0> accepting AMQP connection <0.2009.0> (192.168.96.21:60016 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:34.011172+00:00 [info] <0.2009.0> connection <0.2009.0> (192.168.96.21:60016 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_0          | {}
sum_top_0          | {}
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_0          | listo
sum_top_2          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_0          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_2          | listo
sum_top_0          | listo
sum_top_0          | llega msg
sum_top_0          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_0          | listo
sum_top_0          | ckpt
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_0          | end
rabbitmq           | 2026-11-27 23:59:35.098759+00:00 [info] <0.1976.0> closing AMQP connection <0.1976.0> (192.168.96.21:60008 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
sum_top_1          | llega msg
sum_top_1          | procesado
rabbitmq           | 2026-11-27 23:59:35.102938+00:00 [info] <0.1987.0> closing AMQP connection <0.1987.0> (192.168.96.21:60010 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
rabbitmq           | 2026-11-27 23:59:35.109067+00:00 [info] <0.1998.0> closing AMQP connection <0.1998.0> (192.168.96.21:60014 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
sum_top_1          | listo
rabbitmq           | 2026-11-27 23:59:35.123689+00:00 [info] <0.2009.0> closing AMQP connection <0.2009.0> (192.168.96.21:60016 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
sum_top_2          | end
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
rabbitmq           | 2026-11-27 23:59:35.327403+00:00 [info] <0.2036.0> accepting AMQP connection <0.2036.0> (192.168.96.22:55266 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:35.329860+00:00 [info] <0.2036.0> connection <0.2036.0> (192.168.96.22:55266 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:35.334296+00:00 [info] <0.2047.0> accepting AMQP connection <0.2047.0> (192.168.96.22:55274 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:35.336545+00:00 [info] <0.2047.0> connection <0.2047.0> (192.168.96.22:55274 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | end
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
rabbitmq           | 2026-11-27 23:59:35.679865+00:00 [info] <0.2058.0> accepting AMQP connection <0.2058.0> (192.168.96.23:37184 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:35.684630+00:00 [info] <0.2058.0> connection <0.2058.0> (192.168.96.23:37184 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:35.689589+00:00 [info] <0.2069.0> accepting AMQP connection <0.2069.0> (192.168.96.23:37196 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:35.696516+00:00 [info] <0.2069.0> connection <0.2069.0> (192.168.96.23:37196 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:35.701629+00:00 [info] <0.2080.0> accepting AMQP connection <0.2080.0> (192.168.96.23:37212 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:35.703374+00:00 [info] <0.2080.0> connection <0.2080.0> (192.168.96.23:37212 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:35.710104+00:00 [info] <0.2091.0> accepting AMQP connection <0.2091.0> (192.168.96.23:37220 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:35.714549+00:00 [info] <0.2091.0> connection <0.2091.0> (192.168.96.23:37220 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_2          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
[Ksum_top_0 exited with code 0
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
rabbitmq           | 2026-11-27 23:59:36.417888+00:00 [info] <0.2102.0> accepting AMQP connection <0.2102.0> (192.168.96.24:36372 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.420320+00:00 [info] <0.2102.0> connection <0.2102.0> (192.168.96.24:36372 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.435866+00:00 [info] <0.2113.0> accepting AMQP connection <0.2113.0> (192.168.96.24:36384 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.440460+00:00 [info] <0.2113.0> connection <0.2113.0> (192.168.96.24:36384 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
rabbitmq           | 2026-11-27 23:59:36.682212+00:00 [info] <0.2124.0> accepting AMQP connection <0.2124.0> (192.168.96.25:37636 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.686067+00:00 [info] <0.2124.0> connection <0.2124.0> (192.168.96.25:37636 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.690145+00:00 [info] <0.2135.0> accepting AMQP connection <0.2135.0> (192.168.96.25:37638 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.692339+00:00 [info] <0.2135.0> connection <0.2135.0> (192.168.96.25:37638 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
rabbitmq           | 2026-11-27 23:59:36.715012+00:00 [info] <0.2146.0> accepting AMQP connection <0.2146.0> (192.168.96.26:43938 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.724876+00:00 [info] <0.2149.0> accepting AMQP connection <0.2149.0> (192.168.96.25:37644 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.737314+00:00 [info] <0.2146.0> connection <0.2146.0> (192.168.96.26:43938 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.743610+00:00 [info] <0.2149.0> connection <0.2149.0> (192.168.96.25:37644 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.763919+00:00 [info] <0.2168.0> accepting AMQP connection <0.2168.0> (192.168.96.25:37656 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.767417+00:00 [info] <0.2171.0> accepting AMQP connection <0.2171.0> (192.168.96.26:43942 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.769849+00:00 [info] <0.2171.0> connection <0.2171.0> (192.168.96.26:43942 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.769871+00:00 [info] <0.2176.0> accepting AMQP connection <0.2176.0> (192.168.96.27:44764 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.770156+00:00 [info] <0.2168.0> connection <0.2168.0> (192.168.96.25:37656 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.774691+00:00 [info] <0.2176.0> connection <0.2176.0> (192.168.96.27:44764 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.784720+00:00 [info] <0.2201.0> accepting AMQP connection <0.2201.0> (192.168.96.27:44774 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.787704+00:00 [info] <0.2201.0> connection <0.2201.0> (192.168.96.27:44774 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.792234+00:00 [info] <0.2212.0> accepting AMQP connection <0.2212.0> (192.168.96.27:44776 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.802694+00:00 [info] <0.2212.0> connection <0.2212.0> (192.168.96.27:44776 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-27 23:59:36.820985+00:00 [info] <0.2223.0> accepting AMQP connection <0.2223.0> (192.168.96.27:44786 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-27 23:59:36.826823+00:00 [info] <0.2223.0> connection <0.2223.0> (192.168.96.27:44786 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | end
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | end
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | end
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
[Kmaestro_2 exited with code 0
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | end
sum_top_1          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
[Kmaestro_0 exited with code 0
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
[Kmaestro_1 exited with code 0
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
cliente_0          | vamos por EN 0 - FR 1 en 0.18
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_2          | end
sum_top_1          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | end
sum_top_1          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | end
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_1          | end
sum_top_2          | end
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | listo
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | end
sum_top_2          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | ckpt
sum_top_2          | end
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_1          | end
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_2          | ckpt
cliente_0          | vamos por EN 1 - FR 2 en 0.35
cliente_0          | Tiempo de envio de mensajes: 0.35 minutos
rabbitmq           | 2026-11-27 23:59:51.465450+00:00 [info] <0.1146.0> closing AMQP connection <0.1146.0> (192.168.96.3:45142 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
rabbitmq           | 2026-11-27 23:59:51.468777+00:00 [info] <0.1157.0> closing AMQP connection <0.1157.0> (192.168.96.3:45154 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
rabbitmq           | 2026-11-27 23:59:51.470422+00:00 [info] <0.1168.0> closing AMQP connection <0.1168.0> (192.168.96.3:45156 -> 192.168.96.2:5672, vhost: '/', user: 'guest')[0m
sum_top_1          | llego EOF
sum_top_1          | ckpt
sum_top_2          | end
sum_top_2          | llego EOF
sum_top_2          | llego EOF
sum_top_2          | llega msg
sum_top_2          | procesado
sum_top_2          | listo
sum_top_1          | end
sum_top_2          | llego EOF
sum_top_1          | llega msg
sum_top_1          | procesado
sum_top_1          | listo
sum_top_1          | llego EOF
sum_top_1          | llego EOF
[Knodo-base-1 exited with code 0
rabbitmq           | 2026-11-28 00:00:05.982790+00:00 [info] <0.2336.0> accepting AMQP connection <0.2336.0> (192.168.96.21:47438 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-28 00:00:05.986037+00:00 [info] <0.2336.0> connection <0.2336.0> (192.168.96.21:47438 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-28 00:00:05.992015+00:00 [info] <0.2347.0> accepting AMQP connection <0.2347.0> (192.168.96.21:47450 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-28 00:00:05.994945+00:00 [info] <0.2347.0> connection <0.2347.0> (192.168.96.21:47450 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-28 00:00:05.998523+00:00 [info] <0.2358.0> accepting AMQP connection <0.2358.0> (192.168.96.21:47452 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-28 00:00:06.000044+00:00 [info] <0.2358.0> connection <0.2358.0> (192.168.96.21:47452 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
rabbitmq           | 2026-11-28 00:00:06.003637+00:00 [info] <0.2369.0> accepting AMQP connection <0.2369.0> (192.168.96.21:47458 -> 192.168.96.2:5672)[0m
rabbitmq           | 2026-11-28 00:00:06.005639+00:00 [info] <0.2369.0> connection <0.2369.0> (192.168.96.21:47458 -> 192.168.96.2:5672): user 'guest' authenticated and granted access to vhost '/'[0m
cliente_0          | fin 1795824021.6377926
cliente_0          | Tiempo de envio de mensajes: 0.85 minutos
[Kcliente_0 exited with code 0
Gracefully Stopping... press Ctrl+C again to force
[K Container join_top_2  [32mStopping[0m
[K Container maestro_1  [32mStopping[0m
[K Container maestro_2  [32mStopping[0m
[K Container agregador_top_2  [32mStopping[0m
[K Container promedio_1  [32mStopping[0m
[K Container join_top_1  [32mStopping[0m
[K Container cuenta_prom_2  [32mStopping[0m
[K Container sum_top_1  [32mStopping[0m
[K Container agregador_top_1  [32mStopping[0m
[K Container promedio_2  [32mStopping[0m
[K Container sum_top_2  [32mStopping[0m
[K Container maestro_0  [32mStopping[0m
[K Container img_descargador_1  [32mStopping[0m
[K Container cuenta_prom_1  [32mStopping[0m
[K Container cliente_0  [32mStopping[0m
[K Container maestro_2  [32mStopped[0m
[K Container img_descargador_0  [32mStopping[0m
[K Container maestro_1  [32mStopped[0m
[K Container maestro_0  [32mStopped[0m
[K Container agregador_top_0  [32mStopping[0m
[K Container sum_top_0  [32mStopping[0m
[K Container cuenta_prom_0  [32mStopping[0m
[K Container cliente_0  [32mStopped[0m
[K Container promedio_0  [32mStopping[0m
[K Container join_top_0  [32mStopping[0m
[K Container join_top_1  [32mStopped[0m
[K Container cuenta_prom_2  [32mStopped[0m
[K Container sum_top_2  [32mStopped[0m
[K Container agregador_top_2  [32mStopped[0m
[K Container join_top_0  [32mStopped[0m
[K Container sum_top_1  [32mStopped[0m
[K Container agregador_top_1  [32mStopped[0m
[K Container cuenta_prom_1  [32mStopped[0m
[K Container agregador_top_0  [32mStopped[0m
[K Container promedio_2  [32mStopped[0m
[K Container promedio_1  [32mStopped[0m
[K Container promedio_0  [32mStopped[0m
[K Container sum_top_0  [32mStopped[0m
[K Container join_top_2  [32mStopped[0m
[K Container cuenta_prom_0  [32mStopped[0m
[K Container transformador_1  [32mStopping[0m
[K Container transformador_0  [32mStopping[0m
[K Container transformador_2  [32mStopping[0m
[K Container img_descargador_0  [32mStopped[0m
[K Container img_descargador_1  [32mStopped[0m
[K Container transformador_1  [32mStopped[0m
[K Container transformador_0  [32mStopped[0m
[K Container transformador_2  [32mStopped[0m
[K Container clasificador_2  [32mStopping[0m
[K Container clasificador_2  [32mStopped[0m
[K Container clasificador_1  [32mStopping[0m
[K Container clasificador_1  [32mStopped[0m
[K Container clasificador_0  [32mStopping[0m
[K Container clasificador_0  [32mStopped[0m
[K Container tpg-7574-wikipedia-nodo-base-1  [32mStopping[0m
[K Container gateway  [32mStopping[0m
[K Container tpg-7574-wikipedia-nodo-base-1  [32mStopped[0m
[K Container gateway  [32mStopped[0m
[K Container rabbitmq  [32mStopping[0m
[K Container rabbitmq  [32mStopped[0m
