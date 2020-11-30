function [output] = run_opf_dc(data_name, dist_scale)
    % load the case data
    define_constants;
    mpc = loadcase(data_name);
    mpopt = mpoption('verbose', 0, 'out.all', 1);

    % create the uncertainty
    P_w = [];
    Q_w = [];

    shape = size(mpc.bus);
    for row_idx = 1:shape(1)
        mean = 0;
        P_std = abs(dist_scale * mpc.bus(row_idx, 3));
        P_uncertainty = normrnd(mean,P_std);
        P_w(end+1) = P_uncertainty;
        mpc.bus(row_idx, 3) = mpc.bus(row_idx, 3) - P_uncertainty;

        Q_std = abs(dist_scale * mpc.bus(row_idx, 4));
        Q_uncertainty = normrnd(mean,Q_std);
        Q_w(end+1) = Q_uncertainty;
        mpc.bus(row_idx, 4) = mpc.bus(row_idx, 4) - Q_uncertainty;
    end

    % run dc-opf solver
    results = rundcopf(mpc, mpopt);

    % store the useful solution info
    Pg = results.gen(:, PG);
    Pd = mpc.bus(:, 3);
    Qd = mpc.bus(:, 4);
    F_act = results.branch(:, PF);
    F_max = mpc.branch(:, 6);
    % GB_map = mpc.gen(:, 1);
    % B_idx = mpc.bus(:, 1);
    % Pg_lim = mpc.gen(:, 9:10);

    output = struct('Pg', Pg, 'Pd', Pd, 'Qd', Qd, ...
                    'F_act', F_act, 'F_max', F_max);
    % output = struct('mpc', mpc, 'results', results);

end
