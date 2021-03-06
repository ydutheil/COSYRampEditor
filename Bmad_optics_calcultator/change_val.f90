module change_val_mod
contains
  subroutine change_val(vec, momentum, particle, err_flag_trans)

    use bmad
    use lat_ele_loc_mod
    use comm_vals

    implicit none


    real(dp) :: vec(:), beta, p0c, gamma, momentum
    logical :: err_flag=.false.
    integer :: status
    logical :: err_flag_trans

    
    integer :: i 

    integer :: n_loc
    type (ele_pointer_struct), allocatable :: ele_p_array(:)
    character*250 :: list_ele
    character*100 :: particle


    if( allocated(ele_p_array) ) deallocate( ele_p_array)
    list_ele = 'MXS MXL MXG MX02 MX03 MX04 MX10 MX11 MX12 MX13 QTov1 QTov2 QTov3 QTov4 QTov5 QTov6 QTov7 QTov8 QUov1 QUov2 QUov3 QUov4 QUov5 QUov6 CAVITY BEGINNING QPAX1 QPAX2 QPAX1B QPAX2B'
    !           1   2   3   4    5    6    7    8    9    10   11    12    13    14    15    16    17    18    19    20    21    22    23    24    25     26        27    28    29     30
    call lat_ele_locator (list_ele, lat, ele_p_array, n_loc)

    
    !particle
    if( particle == 'deuteron' ) then 
       lat%param%particle = deuteron$
    elseif( particle == 'proton' ) then
       lat%param%particle = proton$
    endif
    
    ! ! SEXTUPOLES
    ele_p_array(1)%ele%control_var(1)%value = vec(1)
    ele_p_array(2)%ele%control_var(1)%value = vec(2)
    ele_p_array(3)%ele%control_var(1)%value = vec(3)

    
    do i=4, 10
       ele_p_array(i)%ele%value(k2$) = vec(i)
    enddo

    ! QUADRUPOLES
    do i=11, 24
       ele_p_array(i)%ele%control_var(1)%value = vec(i)
    enddo

    ! ! RF voltage
    ! ele_p_array(25)%ele%value(voltage$) = vec(25)

    ! ! Momentum in eV/c
    ele_p_array(26)%ele%value(P0C$) = momentum
    call set_flags_for_changed_attribute ( ele_p_array(26)%ele, ele_p_array(26)%ele%value(p0c$) )
    ! p0c = sqrt((vec(26)/anomalous_moment_of(lat%param%particle))**2-1)*mass_of(lat%param%particle)
    ! gamma = vec(26)/anomalous_moment_of(lat%param%particle)
    ! ele_p_array(26)%ele%value(P0C$)       = p0c
    ! ele_p_array(26)%ele%value(P0C_start$) = p0c
    ! ele_p_array(26)%ele%value(E_tot$) = gamma*mass_of(lat%param%particle)


    !PAX quadrupoles
    ! ele_p_array(27)%ele%value(k1$) = -3.5431
    ! ele_p_array(28)%ele%value(k1$) =  3.6673
    ! ele_p_array(29)%ele%value(k1$) = -3.5431
    ! ele_p_array(30)%ele%value(k1$) =  3.6673

    call set_flags_for_changed_attribute(lat)

    call lattice_bookkeeper(lat)

    do i=1, lat%n_ele_max
       call lat_make_mat6 (lat, i, err_flag=err_flag)
    enddo
    call lattice_bookkeeper(lat)
    call twiss_at_start (lat, status)
    if(   status.ne.ok$) then
          err_flag_trans = .true.
          return
    endif

    call twiss_propagate_all (lat, err_flag=err_flag_trans)
    

  end subroutine change_val

end module change_val_mod

