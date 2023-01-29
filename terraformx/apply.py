def apply(args):
    print("terraformx apply")
    print(args)
    print(args.var_file)
    print(args.auto_approve)
    print(args.refresh_only)

    var_file = args.var_file
    auto_approve = args.auto_approve
    refresh_only = args.refresh_only