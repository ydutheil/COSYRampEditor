program test
use bmad                 ! Define the structures we need to know about.
use comm_vals
use change_val_mod
implicit none
type (ele_struct), pointer :: ele
integer i, ix, n_loc
logical err
type (normal_modes_struct), target :: modes
type (rad_int_all_ele_struct), target ::  ele_rad_int


! tracking
type (coord_struct), allocatable :: orbit(:)
integer i_turn, n_turn, track_state
logical err_flag
real(rp) chromX, chromY, deltaE, momentum

  real(dp) :: vector(26)
  character(100) :: txt100, particle

  vector = 0._rp
  call get_command_argument(1, txt100)
  read(txt100,*) momentum
  call get_command_argument(2, txt100)
  read(txt100,*) particle
  do i =3, 16
     call get_command_argument(i, txt100)
     read(txt100,*) vector(i+8)
  enddo

  ! input is
  ! momentum particle  QTov1 QTov2 QTov3 QTov4 QTov5 QTov6 QTov7 QTov8 QUov1 QUov2 QUov3 QUov4 QUov5 QUov6
  !


! Programs should always implement "intelligent bookkeeping".
bmad_com%auto_bookkeeper = .false.

call bmad_parser ("./COSY_lattice/COSY.bmad", lat)  ! Read in a lattice.
call set_on_off (rfcavity$, lat, off$)

call change_val( vector, momentum, particle, err_flag)

if(err_flag) then
   print *, 'failed'
   print *,  lat%n_ele_track
   stop
endif

call reallocate_coord (orbit, lat)
lat%beam_start%vec = [0.000, 0.000, 0.000, 0.000, 0.000, 0.000] 
call init_coord (orbit(0), lat%beam_start%vec, lat%ele(0), downstream_end$, lat%param%particle)
call track_all (lat, orbit, 0, track_state, err_flag)
call radiation_integrals (lat, orbit, modes, rad_int_by_ele = ele_rad_int)
print *, 1/sqrt(modes%synch_int(1)/ lat%param%total_length)

deltaE = 1.d-4  
call chrom_calc(lat, deltaE, chromX, chromY)
print *, deltaE, chromX, chromY
print *, lat%ele(lat%n_ele_track)%a%phi/(2*pi), lat%ele(lat%n_ele_track)%b%phi/(2*pi)

 
! stop 
! write(300, *) '# Ix Name              ElemType                   s                 BetaX              BetaY            AlphaX            AlphaY             phiX              phiY              Dx                Dpx'
! write(300, *) '# 1  2                 3                          4                 5                  6                7                 8                  9                 10                11                12 '


do i = 0, lat%n_ele_track
  ele => lat%ele(i)
  ! write(*, '(i4,2x,a16,2x,a,20f18.9)') i, ele%name, key_name(ele%key), ele%s, &
  !      ele%a%beta, ele%b%beta, ele%a%alpha, ele%b%alpha, ele%a%phi, ele%b%phi, ele%a%eta, ele%a%etap
  write(*, '(i4,            20f18.9)') i,                              ele%s, &
       ele%a%beta, ele%b%beta, ele%a%alpha, ele%b%alpha, ele%a%phi, ele%b%phi, ele%a%eta, ele%a%etap


enddo
print *,  lat%n_ele_track
end program
